
#----------------------------------------------------------------------------------------------------
# Nightly Replica Sync Script
# This script performs a nightly synchronization of an enterprise geodatabase replica setup,    
# where a staging (parent) geodatabase is reconciled and posted into a target version, 
# then changes are synchronized to a production (child) geodatabase.
# It also includes optional compression steps for maintenance.
# Date: 2026-02-06
# Owner: Joe Hayes 
#----------------------------------------------------------------------------------------------------

import argparse
import datetime as dt
import json
import logging
import os
import sys
import traceback

import arcpy


# -----------------------------
# Logging helpers
# -----------------------------
def setup_logger(log_path: str, level=logging.INFO) -> logging.Logger:
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger = logging.getLogger("gdb_replica_sync")
    logger.setLevel(level)
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(level)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    sh.setLevel(level)
    logger.addHandler(sh)

    return logger


def arcpy_messages() -> str:
    """Return ArcPy messages for better diagnostics."""
    try:
        return arcpy.GetMessages()
    except Exception:
        return ""


# -----------------------------
# Core workflow steps
# -----------------------------
def reconcile_and_post(
    logger: logging.Logger,
    staging_sde: str,
    target_version: str,
    reconcile_mode: str = "ALL_VERSIONS",
    acquire_locks: str = "LOCK_ACQUIRED",
    abort_if_conflicts: str = "NO_ABORT",
    conflict_definition: str = "BY_OBJECT",
    conflict_resolution: str = "FAVOR_TARGET_VERSION",
    with_post: str = "POST",
    with_delete: str = "KEEP_VERSION",
    reconcile_log: str | None = None,
):
    """
    Reconcile and post versions into target_version on a traditionally versioned EGDB.

    Notes:
      - Requires appropriate permissions and that editors are not actively editing versions.
      - For branch versioning, Reconcile Versions uses feature service URLs and different patterns.
    """
    logger.info("Reconcile/Post: workspace=%s target_version=%s", staging_sde, target_version)

    if reconcile_log:
        os.makedirs(os.path.dirname(reconcile_log), exist_ok=True)

    # Set geoprocessing workspace to staging EGDB
    arcpy.env.workspace = staging_sde

    # ReconcileVersions_management signature varies slightly across versions;
    # this call uses the classic parameter order commonly supported.
    # If your environment differs, adjust accordingly (ArcGIS Pro tool reference).
    arcpy.management.ReconcileVersions(
        staging_sde,
        reconcile_mode,
        target_version,
        "",                 # edit_versions (blank when reconcile_mode is ALL_VERSIONS)
        acquire_locks,
        abort_if_conflicts,
        conflict_definition,
        conflict_resolution,
        with_post,
        with_delete,
        reconcile_log if reconcile_log else ""
    )

    logger.info("Reconcile/Post completed.")


def compress_geodatabase(logger: logging.Logger, sde_admin_conn: str):
    """
    Compress an enterprise geodatabase. Must be executed by the geodatabase administrator
    and applies to traditionally versioned enterprise geodatabases.
    """
    logger.info("Compress: %s", sde_admin_conn)
    arcpy.management.Compress(sde_admin_conn)
    logger.info("Compress completed.")


def synchronize_changes(
    logger: logging.Logger,
    parent_sde: str,
    child_sde: str,
    replica_name: str,
    direction: str = "FROM_GEODATABASE_1_TO_2",
    conflict_policy: str = "IN_FAVOR_OF_GDB1",
    conflict_definition: str = "BY_OBJECT",
    reconcile: str = "DO_NOT_RECONCILE"
):
    """
    Synchronize updates between replica geodatabases.

    Recommended for your workflow:
      - parent_sde = Staging (Parent)
      - child_sde  = Production (Child)
      - direction  = FROM_GEODATABASE_1_TO_2
    """
    logger.info(
        "Synchronize Changes: parent=%s child=%s replica=%s direction=%s",
        parent_sde, child_sde, replica_name, direction
    )

    arcpy.management.SynchronizeChanges(
        parent_sde,
        replica_name,
        child_sde,
        direction,
        conflict_policy,
        conflict_definition,
        reconcile
    )

    logger.info("Synchronize Changes completed.")


# -----------------------------
# Main
# -----------------------------
def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Staging (Parent) -> Production (Child) geodatabase replica sync using ArcPy."
    )

    parser.add_argument("--config", help="Path to JSON config file. If provided, overrides other args.", default=None)

    parser.add_argument("--parent-sde", help="Path to Parent (Staging) .sde connection", default=None)
    parser.add_argument("--child-sde", help="Path to Child (Production) .sde connection", default=None)
    parser.add_argument("--replica", help="Replica name as shown in Manage Replicas", default=None)

    parser.add_argument("--target-version", help="Target version to post into (e.g., sde.DEFAULT)", default="sde.DEFAULT")

    parser.add_argument("--do-reconcile-post", action="store_true", help="Run reconcile/post on staging before sync")
    parser.add_argument("--do-compress-parent", action="store_true", help="Compress parent (staging) after reconcile/post")
    parser.add_argument("--do-compress-child", action="store_true", help="Compress child (prod) after sync")

    parser.add_argument("--log-dir", help="Directory for logs", default=r"C:\ArcGIS\Logs\ReplicaSync")
    parser.add_argument("--log-name", help="Log file name prefix", default="nightly_replica_sync")

    args = parser.parse_args()

    cfg = {}
    if args.config:
        cfg = load_config(args.config)

    parent_sde = cfg.get("parent_sde") or args.parent_sde
    child_sde = cfg.get("child_sde") or args.child_sde
    replica_name = cfg.get("replica") or args.replica
    target_version = cfg.get("target_version") or args.target_version

    do_reconcile_post = cfg.get("do_reconcile_post", False) or args.do_reconcile_post
    do_compress_parent = cfg.get("do_compress_parent", False) or args.do_compress_parent
    do_compress_child = cfg.get("do_compress_child", False) or args.do_compress_child

    if not parent_sde or not child_sde or not replica_name:
        raise SystemExit("ERROR: Must provide --parent-sde, --child-sde, and --replica (or via --config).")

    # Logging
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(args.log_dir, f"{args.log_name}_{ts}.log")
    logger = setup_logger(log_path)

    logger.info("=== Replica Sync Started ===")
    logger.info("Parent (Staging): %s", parent_sde)
    logger.info("Child (Prod):     %s", child_sde)
    logger.info("Replica:          %s", replica_name)
    logger.info("Target Version:   %s", target_version)
    logger.info("Options: reconcile_post=%s compress_parent=%s compress_child=%s",
                do_reconcile_post, do_compress_parent, do_compress_child)

    # ArcPy environment
    arcpy.env.overwriteOutput = True

    try:
        # 1) Reconcile/Post on parent (staging) - recommended for traditional versioning workflows
        if do_reconcile_post:
            reconcile_log = os.path.join(args.log_dir, f"reconcile_{ts}.txt")
            reconcile_and_post(
                logger=logger,
                staging_sde=parent_sde,
                target_version=target_version,
                reconcile_mode="ALL_VERSIONS",
                acquire_locks="LOCK_ACQUIRED",
                abort_if_conflicts="NO_ABORT",
                conflict_definition="BY_OBJECT",
                conflict_resolution="FAVOR_TARGET_VERSION",
                with_post="POST",
                with_delete="KEEP_VERSION",
                reconcile_log=reconcile_log
            )

        # 2) Compress parent (staging)
        if do_compress_parent:
            compress_geodatabase(logger, parent_sde)

        # 3) Synchronize (Parent -> Child)
        synchronize_changes(
            logger=logger,
            parent_sde=parent_sde,
            child_sde=child_sde,
            replica_name=replica_name,
            direction="FROM_GEODATABASE_1_TO_2",
            conflict_policy="IN_FAVOR_OF_GDB1",
            conflict_definition="BY_OBJECT",
            reconcile="DO_NOT_RECONCILE"
        )

        # 4) Compress child (prod) - optional
        if do_compress_child:
            compress_geodatabase(logger, child_sde)

        logger.info("=== Replica Sync Completed Successfully ===")

    except arcpy.ExecuteError:
        logger.error("ArcPy ExecuteError occurred.")
        logger.error(arcpy_messages())
        logger.error(traceback.format_exc())
        sys.exit(2)

    except Exception:
        logger.error("Unhandled exception occurred.")
        logger.error(arcpy_messages())
        logger.error(traceback.format_exc())
        sys.exit(3)


if __name__ == "__main__":
    main()