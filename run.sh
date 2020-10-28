#!/bin/bash -l

[ -d logs ] || mkdir logs

echo "Running Devito tests"
devito_file=logs/devito-rtm.txt
rm -f $devito_file

for n in `seq 100 100 400`
do

    info=$( { /usr/bin/time --format \
           'wall-clock time (s): %e\nmemory (kbytes): %M' \
           python devito_rtm.py -d $n $n -tn 2380 --nbl 0 -so 4; \
           } 2>&1 )

    if [ $? -eq 0 ]
    then
        echo "$info"
        run_time=$(echo "$info" | grep "wall" |& grep -oP \
            '(?<=(s)\): ).*')
        memory=$(echo "$info" | grep "memory" |& grep -oP \
            '(?<=(kbytes)\): ).*')

        echo "$n $run_time $memory" >> $devito_file

    else
        echo "Failed — perhaps low memory"
        echo "$n -1 -1" >> $devito_file
    fi
done

rclone copy --progress $devito_file GTDropbox:scaling-test/aws/



echo "Running PyTorch CPU tests"
torch_file=logs/torch-rtm.txt
rm -f $torch_file

for n in `seq 100 100 400`
do

    info=$( { /usr/bin/time --format \
           'wall-clock time (s): %e\nmemory (kbytes): %M' \
           python rtm_pytorch.py $n $n; } 2>&1 )

    if [ $? -eq 0 ]
    then
        echo "$info"
        run_time=$(echo "$info" | grep "wall" |& grep -oP \
            '(?<=(s)\): ).*')
        memory=$(echo "$info" | grep "memory" |& grep -oP \
            '(?<=(kbytes)\): ).*')

        echo "$n $run_time $memory" >> $torch_file

    else
        echo "Failed — perhaps low memory"
        echo "$n -1 -1" >> $torch_file
    fi
done

rclone copy --progress $torch_file GTDropbox:scaling-test/aws/
