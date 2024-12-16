#!/bin/bash

# Check if directory argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    echo "Example: $0 ./logs"
    exit 1
fi

# Get the directory path from argument
DIR_PATH="$1"

# Check if directory exists
if [ ! -d "$DIR_PATH" ]; then
    echo "Error: Directory '$DIR_PATH' does not exist"
    exit 1
fi

# Create/overwrite the output CSV file with headers
echo "instance,seed,population_size,elite_percentage,mutants_percentage,num_independent_populations,vertices,best_cost,total_iterations,last_update_iteration,total_time,last_update_time,path_relink_time,path_relink_calls,num_improvements_elite,num_improvements_best" > results.csv

# Process each .txt file in the specified directory
for file in "$DIR_PATH"/*.txt; do
    # Skip if no txt files found
    [ -e "$file" ] || continue
    
    echo "Processing file: $file"
    
    # Initialize variables for each experiment
    instance=""
    seed=""
    population_size=""
    elite_percentage=""
    mutants_percentage=""
    num_independent_populations=""
    vertices=""
    best_cost=""
    total_iterations=""
    last_update_iteration=""
    total_time=""
    last_update_time=""
    path_relink_time=""
    path_relink_calls=""
    num_improvements_elite=""
    num_improvements_best=""
    
    # Read the file line by line
    while IFS= read -r line; do
        # Extract instance name
        if [[ $line =~ "> Instance: instances/"(.+)\.col ]]; then
            instance="${BASH_REMATCH[1]}"
        fi
        
        # Extract seed
        if [[ $line =~ "> Seed: "([0-9]+) ]]; then
            seed="${BASH_REMATCH[1]}"
        fi
        
        # Extract algorithm parameters
        if [[ $line =~ "population_size "([0-9]+) ]]; then
            population_size="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "elite_percentage "([0-9.]+) ]]; then
            elite_percentage="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "mutants_percentage "([0-9.]+) ]]; then
            mutants_percentage="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "num_independent_populations "([0-9]+) ]]; then
            num_independent_populations="${BASH_REMATCH[1]}"
        fi
        
        # Extract number of vertices
        if [[ $line =~ "Number of vertices: "([0-9]+) ]]; then
            vertices="${BASH_REMATCH[1]}"
        fi
        
        # Extract best cost
        if [[ $line =~ "% Best cost: "([0-9]+) ]]; then
            best_cost="${BASH_REMATCH[1]}"
        fi
        
        # Extract iterations and time information
        if [[ $line =~ "Total number of iterations: "([0-9]+) ]]; then
            total_iterations="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "Last update iteration: "([0-9]+) ]]; then
            last_update_iteration="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "Total optimization time: "([0-9.]+) ]]; then
            total_time="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "Last update time: "([0-9.]+) ]]; then
            last_update_time="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "Total path relink time: "([0-9.]+) ]]; then
            path_relink_time="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "Total path relink calls: "([0-9]+) ]]; then
            path_relink_calls="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "Improvements in the elite set: "([0-9]+) ]]; then
            num_improvements_elite="${BASH_REMATCH[1]}"
        fi
        if [[ $line =~ "Best individual improvements: "([0-9]+) ]]; then
            num_improvements_best="${BASH_REMATCH[1]}"
        fi
        
        # When we find the end marker, write the data
        if [[ $line =~ ^"% Best cost: " ]]; then
            echo "$instance,$seed,$population_size,$elite_percentage,$mutants_percentage,$num_independent_populations,$vertices,$best_cost,$total_iterations,$last_update_iteration,$total_time,$last_update_time,$path_relink_time,$path_relink_calls,$num_improvements_elite,$num_improvements_best" >> results.csv
            
            # Reset variables for next experiment in the same file
            best_cost=""
            total_iterations=""
            last_update_iteration=""
            total_time=""
            last_update_time=""
            path_relink_time=""
            path_relink_calls=""
            num_improvements_elite=""
            num_improvements_best=""
        fi
    done < "$file"
done

echo "Generated results.csv with the following contents:"
cat results.csv