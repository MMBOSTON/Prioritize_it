"""
Script to iterate over each file in the src directory, comparing it with its counterpart in the src_docd directory. 
Uses ndiff from difflib to find differences line by line between corresponding files. 

If differences are found, they're formatted in a way suitable for Markdown rendering and appended to the report string. Finally, the report is saved to Differences_Report.md.

To run this script, ensure you have directories named src and src_docd in the same location as the script, with corresponding files inside them. Adjust src_directory, docd_directory, and report_filename variables as needed based on your actual directory names and desired report file name.

Please note, this script assumes that filenames match exactly between these directories. The compare_files function opens each file, reads its lines, and uses ndiff to find differences. If differences are found, they're formatted in a diff style and appended to the report. The report is then saved to Differences_Report.md. This approach provides a clear, readable format showing additions (+) and deletions (-) between the original and modified files.

This script provides a straightforward comparison and might need adjustments based on the exact structure of your directories and requirements. For example, if your directories contain subdirectories or you need more complex comparisons, you might need to modify the file traversal logic."""

import os
from difflib import ndiff
from pathlib import Path

def compare_files(src_dir, docd_dir, report_file):
    """
    Compares files in src_dir with those in docd_dir and generates a Markdown-formatted differences report.

    Parameters:
    - src_dir (str): Path to the source directory containing original files.
    - docd_dir (str): Path to the target directory containing files with added docstrings.
    - report_file (str): Path to save the differences report in Markdown format.
    """
    src_path = Path(src_dir)
    docd_path = Path(docd_dir)
    
    # Initialize the Markdown report content
    report_md = "# Differences Report\n\n"

    # Iterate over each file in the source directory
    for src_file in src_path.glob('*'):
        if src_file.is_file():
            docd_file = docd_path / src_file.name
            if docd_file.exists():
                # Read both files
                with open(src_file, 'r') as sf, open(docd_file, 'r') as df:
                    src_lines = sf.readlines()
                    docd_lines = df.readlines()
                    
                    # Compare lines using ndiff
                    diff = list(ndiff(src_lines, docd_lines))
                    
                    # Check if there are differences
                    has_diff = False
                    for line in diff:
                        if line.startswith('- ') or line.startswith('+ '):
                            has_diff = True
                            break
                    
                    if has_diff:
                        # Generate a detailed diff for files with differences
                        diff = ''.join(ndiff(src_lines, docd_lines))
                        
                        # Append the diff to the report
                        report_md += f"## Differences in {src_file.name}\n\n"
                        report_md += "```diff\n" 
                        report_md += diff 
                        report_md += "\n"

                    else:
                        report_md += f"No differences found in {src_file.name}\n\n"
                        
    # Write the report to a Markdown file
    with open(report_file, 'w') as rf:
        rf.write(report_md)
        
    print(f"Differences report saved to {report_file}")

def main():
    """
    Main function to execute the comparison and generate the report.
    """
    src_directory = 'src'
    src_docd_directory = 'src_docd'
    src_report_filename = 'src_Differences_Report.md'
    
    input_proc_directory = 'src'
    input_proc_docd_directory = 'src_docd'
    input_proc_report_filename = 'input_proc_Differences_Report.md'

    #compare_files(src_directory, src_directory, src_report_filename)
    
    compare_files(input_proc_directory, input_proc_docd_directory, input_proc_report_filename)

if __name__ == "__main__":
    main()
    
