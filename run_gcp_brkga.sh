#!/bin/bash

# List of instance files
configs=("config1" "config2" "config4" "config5" "config6")
instances=( #"myciel3.col"
    #    "myciel4.col"
    #    "queen5_5.col"
    #    "queen6_6.col"
    #    "myciel5.col"
    #    "queen7_7.col"
    #    "queen8_8.col"
    #    "huck.col"
    #    "jean.col"
    #    "queen9_9.col"
       "david.col"
       "myciel6.col"
       "queen8_12.col"
       "games120.col"
       "queen11_11.col"
       "miles1000.col"
       "miles1500.col"
       "miles250.col"
       "miles500.col"
       "miles750.col"
       "anna.col"
       "queen13_13.col"
       "mulsol.i.3.col"
       "mulsol.i.4.col"
       "mulsol.i.5.col"
       "mulsol.i.2.col"
       "myciel7.col"
       "mulsol.i.1.col"
       "zeroin.i.3.col"
       "zeroin.i.1.col"
       "zeroin.i.2.col"
       "flat300_20_0.col.b"
       "flat300_26_0.col.b"
       "flat300_28_0.col.b"
       "fpsol2.i.3.col"
       "le450_15a.col"
       "le450_15b.col"
       "le450_15c.col"
       "le450_15d.col"
       "le450_25a.col"
       "le450_25b.col"
       "le450_25c.col"
       "le450_25d.col"
       "le450_5a.col"
       "le450_5b.col"
       "le450_5c.col"
       "le450_5d.col"
       "fpsol2.i.2.col"
       "fpsol2.i.1.col"
       "homer.col"
       "inithx.i.3.col"
       "inithx.i.2.col"
       "inithx.i.1.col"
       "flat1000_50_0.col.b"
       "flat1000_60_0.col.b"
       "flat1000_76_0.col.b")


times=("60" "300" "600")
seeds=("298329" "394149" "492929" "593929" "693929")

# Example command:
# julia mainComplete.jl -c config1.conf -s 298329 -r T -a 0 -t 60 -i "instances/myciel3.col"
# Loop through each instance, time, config and seed
for config in "${configs[@]}"; do
    for instance in "${instances[@]}"; do
        for time in "${times[@]}"; do
            for seed in "${seeds[@]}"; do
                # Run the Julia script with the current instance, time, and seed
                echo "Running for instance ${instance}, time ${time}, and seed ${seed}..."
                julia mainComplete.jl -c "${config}.conf" -s ${seed} -r T -a 0 -t ${time} -i "instances/${instance}" >> "Results/log_${instance}_${time}seconds_${config}.txt" 2>&1
                
                # Check if the Julia script ran successfully
                if [ $? -ne 0 ]; then
                    echo "Error running Julia script with ${instance}, time ${time}, and seed ${seed}. Exiting."
                    exit 1
                fi
            done
        done
    done
done

echo "All commands executed successfully."