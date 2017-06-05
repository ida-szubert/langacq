#!/usr/bin/env bash

python2 SemLearn.py i_n -i trainFiles/Adam{}_lf.txt -t my_test/train_test_parses_Adam{}_reps1_ -n my_test/train_train_parses_Adam{}_reps1_ -s 20  --dump_out my_test/train_test_parses_reps1_dump_ --dinter 100 --dump_vr --analyze --dotest
#python2 SemLearn.py i_n -i trainFiles/trainPairs.filtered.ready_{} -t my_test/Eve_train_test_parses_terminal_reps1_ -n my_test/Eve_train_train_parses_terminal_reps1_ -s 21 -m my_test/Eve_model_throwaway.pkl --dump_out my_test/Eve_train_test_parses_terminal_reps1_dump_ --dinter 100 --dump_vr --analyze
