#!/bin/bash

# List of instance files
configs=("config2" "config4" "config5" "config6")
instances=("fpsol2.i.1.col" "fpsol2.i.2.col" "fpsol2.i.3.col" "inithx.i.1.col" "inithx.i.2.col" "inithx.i.3.col" "le450_15a.col" "le450_15b.col" "le450_15c.col" "le450_15d.col" "le450_25a.col" "le450_25b.col" "le450_25c.col" "le450_25d.col" "le450_5a.col" "le450_5b.col" "le450_5c.col" "le450_5d.col" "mulsol.i.1.col" "mulsol.i.2.col" "mulsol.i.3.col" "mulsol.i.4.col" "mulsol.i.5.col" "zeroin.i.1.col" "zeroin.i.2.col" "zeroin.i.3.col" "anna.col" "david.col" "homer.col" "huck.col" "jean.col" "games120.col" "miles1000.col" "miles1500.col" "miles250.col" "miles500.col" "miles750.col" "queen11_11.col" "queen13_13.col" "queen5_5.col" "queen6_6.col" "queen7_7.col" "queen8_12.col" "queen8_8.col" "queen9_9.col" "myciel3.col" "myciel4.col" "myciel5.col" "myciel6.col" "myciel7.col")
times=("60" "180")
seeds=("298329" "394149" "492929" "593929" "693929")

# Do jeito que foi pedido levaria 112 horas (14*6*5*(1+5+10)/60). Deixei com 1 e 3 minutos para rodar em 28 (14*6*5*(1+3)/60).

# Loop through each instance, time, config and seed
for config in "${configs[@]}"; do
    for instance in "${instances[@]}"; do
        for time in "${times[@]}"; do
            for seed in "${seeds[@]}"; do
                # Run the Julia script with the current instance, time, and seed
                echo "Running for instance ${instance}, time ${time}, and seed ${seed}..."
                julia mainComplete.jl -c "configs/${config}.config" -s ${seed} -r T -a 0 -t ${time} -i "data/${instance}.txt" >> "Results/log_${instance}_${time}seconds_${config}.txt" 2>&1
                
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