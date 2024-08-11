# DONE:
- Updated PrioritizeIt with TaskList Class name                                             [OK]
- Merged all Class TaskManager functions to TaskList module                                 [TODO]
- Changed AgGrid to a new name "Spreadsheet Data Analyzer"                                  [OK]
- Changed Core Task Generation to a new name "Demo Data Analyzer"                           [OK]
- Made the AgGrid as the default operation (may put back the check box feature later)       [TODO]
- Made all AgGrid Table columns adjustable and different widths                             [OK]
- Made the Name/Description cell content viewable "ALL" with mouse pointer                  [BROKEN]
   ++ Worked, now broken
- Task_value and Task_effort cells editable                                                 [OK]
- Save updated tasks to JSON and CSV                                                        [OK]
- Automatic Ratio calculation                                                               [OK]
- Update Ratio based on the Value/Effort change dynamically                                 [OK]
- Added a Rank column and calculated based on Value/Effort/Ratio                            [OK]
   ++ Dynamic Rank update is NOT working after any change in Value/Effort                   [TODO]
- Added Cuilitative Effort Curve                                                            [OK]
- Merged/layover Pareto vs Burndown curves                                                  [OK]
- Reassign Task_id to a reasonable task name "Task-0001"                                    [TODO]
   ++ Broken Again
- Task Type Grouping                                                                        [TODO] 
- Unit for Columns                                                                          [TODO]
- Chart by  Group Type or By Task Type                                                      [TODO]
- Moved  "Demo Task Generation" to the sidebar (Broken)                                     [TODO]
- Manual File Uploader                                                                      [TODO]
- Open Form Task Input                                                                      [TODO]
- Have a sidebar with "Instructions" and "Try Demo" to open "Demo Data Analyzer"            [TODO]
- Add "Generate Report" functions                                                           [TODO]
- Add Reset functions                                                                       [TODO]
- Cleaning up unused codes
- DocString Generation                                                                      [TODO]

Data Entry Methods:
+   Spreadsheet Data Analyzer
+   File Upload
+   Manual Task Entry Analyzer

Move the "Automatic Tasks Generation" (FAKER Pack) to Instruction to use for Demo purposes only

TARGET AUDIENCE:
    MVP 1.0 - individual end user
    MVP 2.0 - integrate with other tools



Launch App
Input Tasks (unassigned tasks, blank-separated Name-Description lines, CSV, XLSX) 
Display Tasks
Assign Value & Effort (for ratio and ranking)
	calculate V/E ratio and rank by ratio
Visualize 
Save & Use Ranked Priorities (Track, Export )


Visual GUI Flow 
Instructions display
Data input controls are showing

# Workflow Outline:

# PHASE - Start App
## 01  Start the Streamlit app
## 02. Read "Instructions"

# A) PHASE - Data Input

## 03. Get Data In 
    ### 03a. Import Tabular data (CSV, XLSX, SQL? )
    ### 3b. Import Text data (text ==>, bulleted, lists, structured text (name + description))
    ### 3c. Manual Data Entry Form
    ### [MVP 2+] 3c. Online PM System (Jira, Monday.com, Github Projects, Notion, etc.)
## 04. Validate data entered
## 05. Cleanup if required
## 06. Save Clean Data

# B) PHASE - Data Analysis

## 07a. Assign Task Value & Effort (may already be assigned above)
## 07b. Assign Tasks to Task Groups (for MANY input tasks ==> (MVP 1.1)
## 08. Calculate Value-Effort Ratio
## 09. Rank Priorities (sort) [Ranked by Value-Effort ratio]

# C) PHASE - Data Viz

## 10. Display Results as active visualization ("interactive" ?) 
## 10b. Show Rank by Tasks, by Tasks Group (2 Interactive selection) 
## 11. Review & Approve before generating report
## 12. Generate Report (from ranked data grid and final chart)

# D) PHASE - Reporting

## 13. Save ALL Final Results (Report, grid data, chart)  DONE  !!!!
        Save PDF
        Save to CSV, XLSX, SQL
## 14. Send to other people, places, things


TODO: introduce Task Group concept 
    source_task_id ==> keep the original task data, 
    map it to current Pareto Task Group (map "source_task_id" to "PP_Task_Group")

Separate App:
Simple Tasks Tracker Tool (instead Jira, Taigo, etc....)
