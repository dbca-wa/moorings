#!/bin/bash

# --- Configuration ---
# An array of your frontend application directories.
# These paths are relative to the script's location.
FRONTEND_DIRS=(
    "./admissions"
    "./availability2"
    "./mooring"
    "./exploreparks"
)
# -------------------

echo "Starting all frontend development servers..."
echo "-------------------------------------------"

# Loop through each directory
for dir in "${FRONTEND_DIRS[@]}"; do
    # Check if the directory exists
    if [ -d "$dir" ]; then
        echo "=> Starting server in '$dir'..."
        # Execute `npm run dev` in a subshell and run it in the background (&)
        # This allows the script to continue without waiting for the command to finish.
        (cd "$dir" && npm run dev) &
    else
        echo "Warning: Directory '$dir' not found. Skipping."
    fi
done

echo "-------------------------------------------"
echo "All servers have been launched in the background."
echo "Use './stop_dev.sh' to terminate them all."