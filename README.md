Data Entry Methods:
+   Spreadsheet Data Analyzer
+   File Upload
+   Manual Task Entry Analyzer

Move the "Automatic Tasks Generation" (FAKER Pack) to Instruction to use for Demo purposes only

TARGET AUDIENCE:
    MVP 1.0 - individual end user
    MVP 2.0 - integrate with other tools

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
