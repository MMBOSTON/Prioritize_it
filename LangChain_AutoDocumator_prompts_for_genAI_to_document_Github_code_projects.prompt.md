# Project_Title: AI-Powered Project Documentation Automation Assistant

# Product_Title: "The Documator" Your Docs Doctor.  

- Created_By: Rich Lysakowski
- Created_On: 2024.08.08
- Updated_On: 2024.08.09

# Deliver a Well-documented Codebase

We want to help other developers understand, reuse and maintain this codebase more easily.

## Methodology and Tools

### Methodology: To Be Done

### Tools: This example uses Phind.com

Phind.com is a free-mium plugin for VSCode that can read an entire local folders filled with files.  

Copilot, Claude, Gemini, and other LLM code generators usually refuse to read local files because of personal information security reasons.  Without special plugins for Claude, Gemini, and other LLM code generators, they cannot read entire folders from the local file system.  There are paid subscriptions for GPTs and other AI tools that can read local files, but they usually use LangChain or other special libraries to reach outside the "AI runtime sandbox".  

## Getting Started - Cloning The Repo to Be Documented

1) Make a local clone of your Gitub.com Project repository.  You can use Github Desktop or VS Code to pull the repository to your local system.  

2) Attach all the files that you want documented to the Phind Chatbox. 

### Prompt: Create Project-level Readme.md file: 

Message to Phind: Read the files attached to the chatbox.  

Generate documentation for this entire project. First give me a README.md file that summarizes what the project is for. Then we'll work on individual modules and documenting them.

## Prompt: Create Python Runtime-Environment files:

If the environment.yml (for conda install) or the requirements.txt file (for pip install) is absent, then we will need to create them based on the dependencies in all the Python projectd code files.  

Read through all Python project files, do a dependencies analysis to identify all required package imports.

Then create two files: 

1) requirements.txt for pip installation 
2) environment.yml file for conda installation.  Use conda-forge for all packages if available.  

## Prompt: Create Installation Instructions: 

If the project does not have complete "Setup and Installation Instructions".  If the instructions are missing for building the "runtime environment' using conda virtual environment manager, conda package installations, and "pip install -r requirements.txt" command, then they must be created based on a dependencies analysis of all the Python project code files.  

## Document each code file in each folder added to the processing list.   

We want docstrings that provide a clear explanation of what each module and function does, along with details about their inputs and outputs. 
We want to help other developers understand, reuse and maintain the code more easily.

Report back a separate documented file for each input source file attached to this message.  Ask me clarifying questions if you need to.   

### Prompt: [Optional] If Phind does not read and document all files, or generates only docstrings and not entire code files, or only does one file at a time, then you may have to prompt it several times.  

DOCUMENTATION PROBLEM: Missing Docstrings for the Module?   

Propmt: You did not provide a docstring for the module.  You also did not generate complete files with all the code.  Try again and make sure you generate complete executable files with nothing left out.  Do not provide snippets, fragments, or undone sections.  Use the existing active code VERBATIM, and DO NOT CHANGE ANY ACTIVE CODE; simply add documentation to it.   Are you clear? 

Proceed to the next file.

Proceed to do the rest of the files one at a time.

#####################################################################################
# PROBLEM_LAZY_AI_Agent: Incomplete Files [Fragments, Snippets, partial answers?] 

Prompt: You also did not generate complete files with all the code.  Try again and make sure you generate complete executable files with nothing left out.  Do not provide snippets, fragments, or undone sections.  Use the existing active code VERBATIM, and DO NOT CHANGE ANY ACTIVE CODE; simply add documentation to it.   Are you clear? 

Proceed to the next file.

# AutoDocumator Prompt: Quality Check

Now do a Documator quality check to verify that no executable code was modified during the docstrings generation tasks.  

Compare each file in the original directory named "src" with the corresponding file with the same name in the output target directory named "src_docd".  

Provide an easily-readable differences report for each file, showing all the lines with differences on a line-by-line difference in a wide tabular format.  

Save the Differences Report to a Markdown text file, so that it can be rendered in a browser or other Markdown viewer.    

#####################

Now create a program to do a quality check and report to verify that no executable code was modified during the docstrings generation tasks.  

The functions should do the following tasks: 

Compare each file in the original directory named "src" with the corresponding file with the same name in the output target directory named "src_docd".  

Provide an easily-readable Differences_Report for each source code file checked, showing all the lines with differences on a line-by-line difference in a wide tabular format.  

Save the Differences Report to a Markdown text file, so that it can be rendered in a browser or other Markdown viewer.    

You can use any common Python Standard Library packages that make this task easier.  