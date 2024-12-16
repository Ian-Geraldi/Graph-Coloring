#!/bin/bash

# Create/overwrite the output CSV file with headers
echo "filename,best,worst,average" > results.csv

# Process each .txt file in the current directory
for file in *.txt; do
    # Skip if no txt files found
    [ -e "$file" ] || continue
    
    # Initialize variables for each file
    sum=0
    count=0
    min=""
    max=""
    
    # Read the file line by line
    while IFS= read -r line; do
        # Look for lines containing "% Best cost: "
        if [[ $line =~ "% Best cost: "([0-9]+) ]]; then
            cost="${BASH_REMATCH[1]}"
            
            # Convert cost to number for arithmetic
            cost_num=$((cost))
            
            # Initialize min/max on first value
            if [ -z "$min" ]; then
                min=$cost_num
                max=$cost_num
            fi
            
            # Update min if current cost is lower
            if [ $cost_num -lt $min ]; then
                min=$cost_num
            fi
            
            # Update max if current cost is higher
            if [ $cost_num -gt $max ]; then
                max=$cost_num
            fi
            
            # Add to sum and increment counter for average
            sum=$((sum + cost_num))
            count=$((count + 1))
        fi
    done < "$file"
    
    # Calculate average if we found any values
    if [ $count -gt 0 ]; then
        # Use bc for floating point division
        average=$(echo "scale=2; $sum / $count" | bc)
        
        # Append to CSV file
        echo "$file,$min,$max,$average" >> results.csv
    fi
done

# Print the contents of the CSV file
echo "Generated results.csv with the following contents:"
cat results.csv
