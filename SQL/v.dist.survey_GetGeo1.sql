USE [distribution]
GO

/****** Object:  View [survey].[v_GetGeo1]    Script Date: 3/23/2023 11:00:08 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [survey].[v_GetGeo1]
AS
SELECT DISTINCT 
                  TOP (100) PERCENT WashGEO1.dbo.TLXYAT.TLNO AS tlid, WashGEO1.dbo.OWNRAT.OwnerName, WashGEO1.dbo.OWNRAT.OwnerAddr, WashGEO1.dbo.OWNRAT.OwnerAddr2, WashGEO1.dbo.OWNRAT.OwnerAddr3, 
                  WashGEO1.dbo.OWNRAT.OwnerCity, WashGEO1.dbo.OWNRAT.OwnerState, WashGEO1.dbo.OWNRAT.OwnerZip, WashGEO1.dbo.core_situs_address_table.HOUSE_NUMBER, WashGEO1.dbo.core_situs_address_table.FULLADDRESS, 
                  WashGEO1.dbo.core_situs_address_table.CITY, WashGEO1.dbo.AGGSITEAT.LandVal, WashGEO1.dbo.AGGSITEAT.BldgVal, WashGEO1.dbo.AGGSITEAT.RMVVAL, WashGEO1.dbo.AGGSITEAT.BldgSqft, 
                  WashGEO1.dbo.AGGMISCAT.Acres, WashGEO1.dbo.SITEAT.YearBuilt, WashGEO1.dbo.SITEAT.SaleDate, WashGEO1.dbo.SITEAT.SalePrice, WashGEO1.dbo.OWNRAT.Account, WashGEO1.dbo.TLXYAT.X_Coordinate, 
                  WashGEO1.dbo.TLXYAT.Y_Coordinate
FROM     WashGEO1.dbo.TLXYAT LEFT OUTER JOIN
                  WashGEO1.dbo.OWNRAT ON WashGEO1.dbo.TLXYAT.TLNO = WashGEO1.dbo.OWNRAT.TLNO LEFT OUTER JOIN
                  WashGEO1.dbo.AGGSITEAT ON WashGEO1.dbo.OWNRAT.TLNO = WashGEO1.dbo.AGGSITEAT.TLNO LEFT OUTER JOIN
                  WashGEO1.dbo.SITEAT ON WashGEO1.dbo.AGGSITEAT.TLNO = WashGEO1.dbo.SITEAT.TLNO LEFT OUTER JOIN
                  WashGEO1.dbo.core_situs_address_table ON WashGEO1.dbo.SITEAT.TLNO = WashGEO1.dbo.core_situs_address_table.TAXLOT LEFT OUTER JOIN
                  WashGEO1.dbo.AGGMISCAT ON WashGEO1.dbo.core_situs_address_table.TAXLOT = WashGEO1.dbo.AGGMISCAT.TLNO
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "TLXYAT (WashGEO1.dbo)"
            Begin Extent = 
               Top = 7
               Left = 48
               Bottom = 82
               Right = 242
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "OWNRAT (WashGEO1.dbo)"
            Begin Extent = 
               Top = 7
               Left = 290
               Bottom = 82
               Right = 484
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "AGGSITEAT (WashGEO1.dbo)"
            Begin Extent = 
               Top = 7
               Left = 532
               Bottom = 82
               Right = 726
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "SITEAT (WashGEO1.dbo)"
            Begin Extent = 
               Top = 7
               Left = 774
               Bottom = 82
               Right = 968
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "core_situs_address_table (WashGEO1.dbo)"
            Begin Extent = 
               Top = 7
               Left = 1016
               Bottom = 82
               Right = 1210
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "AGGMISCAT (WashGEO1.dbo)"
            Begin Extent = 
               Top = 7
               Left = 1258
               Bottom = 82
               Right = 1452
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   E' , @level0type=N'SCHEMA',@level0name=N'survey', @level1type=N'VIEW',@level1name=N'v_GetGeo1'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane2', @value=N'nd
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1176
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1356
         SortOrder = 1416
         GroupBy = 1350
         Filter = 1356
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'survey', @level1type=N'VIEW',@level1name=N'v_GetGeo1'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=2 , @level0type=N'SCHEMA',@level0name=N'survey', @level1type=N'VIEW',@level1name=N'v_GetGeo1'
GO

