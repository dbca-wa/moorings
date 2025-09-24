#!/bin/bash

echo "Stopping all Node.js development servers..."

# This command finds and kills processes related to 'vite'.
# If you use other tools like Create React App or Next.js, 
# you might need to change 'vite' to 'react-scripts' or 'next'.
pkill -f "vite"

echo "All development servers should be stopped."