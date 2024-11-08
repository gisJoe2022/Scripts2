USE [distribution]
GO

/****** Object:  View [survey].[v_platsApp1221] on washsde.distribution   Script Date: 3/23/2023 10:56:01 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [survey].[v_platsApp] /* remove lines 11 and 12 if creating using ESRI DB view GP Tool */
AS
SELECT TOP (100) PERCENT plat_main_1.Platname, plat_main_1.[Book/Page] AS BookPage, plat_main_1.Recorded, plat_main_1.DocNumber, Surveyors_1.SurveyorName, plat_main_1.Surveyornumber, plat_main_1.Reserved
FROM     PSQLAPP1.Survey.dbo.Plat_Main AS plat_main_1 LEFT OUTER JOIN
                  PSQLAPP1.Survey.dbo.CityCode AS CityCode_1 ON plat_main_1.City = CityCode_1.CityCode LEFT OUTER JOIN
                  PSQLAPP1.Survey.dbo.Surveyors AS Surveyors_1 ON plat_main_1.Surveyornumber = Surveyors_1.SurveyorNumber
WHERE  (plat_main_1.Reserved = 0)
ORDER BY plat_main_1.Platname
GO

/* EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
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
         Begin Table = "plat_main_1"
            Begin Extent = 
               Top = 7
               Left = 48
               Bottom = 170
               Right = 251
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "CityCode_1"
            Begin Extent = 
               Top = 7
               Left = 299
               Bottom = 148
               Right = 493
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "Surveyors_1"
            Begin Extent = 
               Top = 7
               Left = 541
               Bottom = 148
               Right = 747
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
      Begin ColumnWidths = 9
         Width = 284
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1824
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
' , @level0type=N'SCHEMA',@level0name=N'survey', @level1type=N'VIEW',@level1name=N'v_platsApp'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'survey', @level1type=N'VIEW',@level1name=N'v_platsApp'
GO
 */
