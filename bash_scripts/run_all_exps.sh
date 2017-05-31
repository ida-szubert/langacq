
# set dir = $1

# mkdir ${dir}

set distractors = 1

echo "First python call"

python -u SemLearn.py i_n -i trainFiles/trainPairs.filtered.ready -t my_test/train_test_parses_reps1_ -n my_test/train_train_parses_reps1_ --dump_out my_test/train_test_parses_reps1_dump_ --dinter 100 --dump_vr --analyze --dotest >& my_test/log_1rep_dump_my_test &


for distractors in 3 5 7
do

 echo "python call with $distractors distractors"
python -u SemLearn.py i_n - $distractors -i trainFiles/trainPairs.filtered.ready -t my_test/train_test_parses_reps${distractors}_ -n my_test/train_train_parses_reps$distractors_ --dump_vr --dinter 100 --analyze  --dump_out my_test/train_test_parses_reps$distractors_dump_ --dotest >& my_test/log_${distractors}rep_dump_my_test &

done




