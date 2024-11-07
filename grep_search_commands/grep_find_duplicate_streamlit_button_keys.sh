#!/bin/bash

# Script creates a file named grep_search_results_<datetime>.txt and writes results of each grep command to it.
# The > operator is used to create the file and write the first set of results,
# and the >> operator is used to append the subsequent results to the same file.

# The $output_file variable directs the output of the echo and grep commands to specified file.
# This ensures that all output is collected in one place.

# Get the current datetime in the format YYYYMMDD_HHMMSS
datetime=$(date +"%Y%m%d_%H%M%S")

# Define the output file with the datetime stamp
output_file="grep_search_results_${datetime}.txt"

# Function to run grep and print headers
run_grep() {
    local search_term=$1
    local output_file=$2

    echo "Running grep search for: $search_term" >> "$output_file"
    echo "Results:" >> "$output_file"
    grep -r "$search_term" "C:\Users\PowerUser\Documents\Github_Repos_RSL\Prioritize_it_MMBOSTON\src" >> "$output_file"
    echo "" >> "$output_file"  # Add a blank line for separation
}

# Define Header Information to be printed in the output file:
# The string $output_file at the end of the lines specify the output file to write. 
# In this script, it ensures that the output of the echo commands and the grep command
# is redirected to the file defined by the output_file variable.

echo "Shell Script: grep_search_duplicate_streamlit_button_keys.sh" > "$output_file"
echo "Output File: $output_file" >> "$output_file"
echo "" >> "$output_file"  # Add a blank line for separation

# Run the grep commands and write the results to the output file
run_grep "reset_app_button_sidebar" "$output_file"
run_grep "show_instructions_sidebar" "$output_file"
run_grep "file_conversion_sidebar" "$output_file"
run_grep "interactive_debug_sidebar" "$output_file"

# Print a message indicating the completion of the script
echo "Grep search completed. Results written to: $output_file"

# End of script

# Other grep search examples: 
# grep -r --include="*.py" "reset_app_button_sidebar" "C:\Users\PowerUser\Documents\Github_Repos_RSL\Prioritize_it_MMBOSTON\src"

