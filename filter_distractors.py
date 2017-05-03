#############################################
## This is getting stripped down so that I ##
## can see what the hell is going on.      ##
#############################################
## this needs to be sorted out so that I can do things with it
## want high level options for hyperparameters
## want high level option for one vs many words
## want ONE function to check parses (deal with search problem)
## MAKE INTO SEPARATE FILES



import pdb
import copy
import math
import cPickle
import sys
import random
import os

import verb_repo
from optparse import OptionParser
from math import log
from math import exp
from scipy.special import psi
from timeit import Timer
#from generator import generateSent
from tools import *
from grammar_classes import *
from lexicon_classes import *
from semc import *
from build_inside_outside_chart import *
from inside_outside_calc import *
from parser import *
from sample_most_probable_parse import *
from print_parses import *
from makeGraphs import *

from cat import synCat
import cat
import extract_from_lexicon3
import exp
from semType import semType
from correct_dependencies_with_templates import repFromExample
from correct_dependencies_with_templates import checkIfWh
import readInExps
from errorFunct import error
import expFunctions



def train_rules(sem_store,RuleSet,lexicon,oneWord,inputpairs,
                cats_to_check,output,test_out=None,dotest=False,sentence_count=0,
                min_lex_dump=0, max_lex_dump=1000000,dump_lexicons=False,
                dump_interval=100,dump_out='lexicon_dump',f_out_additional=None,truncate_complex_exps=True,
                verb_repository=None,dump_verb_repo=False,analyze_lexicons=False,output_file=None):
    
    print "testout = ",test_out
    print "put in sent coutn = ",sentence_count
    if not sentence_count: sentence_count = 0
    datasize = 10000
    lexicon.set_learning_rates(datasize)
    wordstocheck = []
    sentstogen = []
    train_limit = 10000
    sentence_charts = {}
    catStore = {}
    sentence_limit = 10
    line_count = 0
    lo = None
    sentence = None
    topCatList = []
    output_file_handle = open(output_file,'w')
    cur_example = []
    
    while line_count < len(inputpairs):
        line = inputpairs[line_count]
        line_count += 1
        if line[:5]=="Sent:":
            isQ = False
            donetest = False
            #print "got sent ",line
            sentence = line[6:].strip().rstrip()
            if sentence.count(" ")>sentence_limit:
                print "rejecting ",line
                sentence = None
                cur_example = []
                continue
            topCatList = []
            sentisq = False
            cur_example.append(line)
        
        if sentence and line[:4]=="Sem:":
            #print "got sem ",line
            semstring = line[5:].strip().rstrip()
            #if semstring.__contains__("^"): continue
            r = expFunctions.makeExpWithArgs(semstring,{})
            if len(r[0].allExtractableSubExps()) > 9 and truncate_complex_exps:
                print "rejecting ",r[0].toString(True)
                for e in r[0].allExtractableSubExps():
                    print e.toString(True)
                r = None
                sentence = None
                cur_example = []
                continue
            sem = None
            if r: sem = r[0]
            else: error("could not make exp")
            
            if checkIfWh(sem):
                isQ = False
                sc = synCat.swh
            elif sem.isQ():#__==exp.qMarker:
                isQ = True
                sc = synCat.q
                if topCatList==[]: sentisq = True
            else:
                isQ = False
                #print "finding cat for ",sem.toString(True)," which has type ",sem.type().toString()
                sc = synCat.allSynCats(sem.type())[0]
            words = sentence.split()#[:-11]
            if not isQ and words[-1] in ["?","."]:
                words = words[:-1]
            else: print "Is Q"
            if len(words)==0:
                words = None
                sentence = None
                sem = None
                sc = None
                cur_example = []
                continue
            topCat = cat.cat(sc,sem)
            topCatList.append(topCat)
            print "sentence is ",sentence
            cur_example.append(line)
        
        if sentence and line[:11]=="example_end":
            if len(words)>8:
                sentence = []
                cur_example = []
                sem = None
                continue
            cur_example.append(line)
            if sem:
                output_file_handle.write(''.join(cur_example)+'\n')
            cur_example = []
    
    print "returning sentence count ",sentence_count
    return sentence_count


##########################################################


def test(test_file,sem_store,RuleSet,Current_Lex,test_out,sentence_count):
    Current_Lex.refresh_all_params(sentence_count)
    retsem = None
    for line in test_file:
        if line[:5] == "Sent:":
            sentence = line[6:].split()
            #if len(sentence)>5: 
        if line[:4] == "Sem:":
            sem = expFunctions.makeExpWithArgs(line[5:].strip().rstrip(),{})[0]
            if not sem.isQ() and sentence[-1] in [".","?"]:
                sentence = sentence[:-1]
            if len(sentence)==0:
                sem = None
                sentence = None
                continue
            print >> test_out,sentence
            retsem = None
            top_parse = None
            (retsem,top_parse,topcat) = parse(sentence,sem_store,RuleSet,Current_Lex,sentence_count,test_out)


            if retsem and sem and retsem.equals(sem):
                print >> test_out, "CORRECT\n"+retsem.toString(True)+"\n"+topcat.toString()
                
            elif not retsem:
                print >> test_out, "NO PARSE"
                continue
            else:
                print >> test_out, "WRONG"
                print >> test_out, retsem.toString(True)+"\n"+topcat.toString()
                print >> test_out,  sem.toString(True)
                if sem and retsem.equalsPlaceholder(sem):
                    print >> test_out, "CORRECTPlaceholder\n"+retsem.toString(True)+"\n"+topcat.toString()
                        
            print >> test_out,'top parse:'
            print >> test_out, top_parse
                #print >> test_out, top.inside_score
            print >> test_out, "\n"




###########################################
# Main.                                   #
# Try to keep to just build or check      #
###########################################

def main(argv,options):
    #print "here"
    print argv
    build_or_check = argv[1]
    if len(argv)>2:
        To = argv[2]
    else:
        To = None
    if len(argv)>3:
        k = argv[3]
    else:
        k = None
    print "build or check is ",build_or_check

    if build_or_check=="i_n": #train on months 1..i, test on the n-th
        exp.exp.allowTypeRaise = False

        # initialization info #
        oneWord = True
        if len(argv)>2 and argv[2] in ["mwe","MWE"]:
            oneWord = False
        numreps = 1
        if len(argv)>3:
            numreps = int(argv[3])
            print('Number of possible LFs in training:'+str(numreps))
        if len(argv)>4:
            extra = argv[4]
        else:
            extra = ""

        reverse = False #True
        if reverse: extra = extra+"reversed"

        Lexicon.set_one_word(oneWord)

        rule_alpha_top = 1.0
        beta_tot = 1.0
        beta_lex = 0.005
        
        verb_repository = verb_repo.VerbRepository()
        RuleSet = Rules(rule_alpha_top,beta_tot,beta_lex)

        type_to_shell_alpha_o = 1000.0
        shell_to_sem_alpha_o = 500.0
        word_alpha_o = 1.0
        
        Current_Lex = Lexicon(type_to_shell_alpha_o,shell_to_sem_alpha_o,word_alpha_o)
        
        RuleSet.usegamma = False
        Current_Lex.usegamma = False
        
        sentence_count = 0
        
        cats_to_check = []
        
        sem_store = SemStore()
        for i in range(1,21):
            input_file = options.inp_file #"trainFiles/trainPairs"
            test_file = options.inp_file   #"trainFiles/trainPairs"

            if numreps > 1:
                input_file = input_file+str(numreps)+"reps"
            output_file = input_file + '.filtered'+"_"+str(i)
            input_file = input_file+"_"+str(i)

            #if numreps > 1:
                #test_file = test_file
            #test_file = test_file+"_"+str(i+1)
            #input_file = input_file+"_"+str(17)
            if reverse: test_file = test_file+"_20"
            else: test_file = test_file+"_20"
            #input_file = "first20train.txt"
            inputpairs = open(input_file).readlines()

            outfile = options.train_parses +'_'
            testoutfile = options.test_parses + '_'
    
            if oneWord:
                outfile = outfile+"1W"
                testoutfile = testoutfile+"1W"
            else:
                outfile = outfile+"MWE"
                testoutfile = testoutfile+"MWE"

            if numreps > 1:
                outfile = outfile+"_"+str(numreps)+"reps"
                testoutfile = testoutfile+"_"+str(numreps)+"reps"

            outfile = outfile+"_"+str(i)
            testoutfile = testoutfile+"_"+str(i)
            output = open(outfile,"w")

            sentence_count = train_rules(sem_store,RuleSet,Current_Lex,oneWord,inputpairs,
                                         cats_to_check,output,None,False,sentence_count,
                                         min_lex_dump=options.min_lex_dump,
                                         max_lex_dump=options.max_lex_dump,
                                         dump_lexicons=options.dump_lexicons,
                                         dump_interval=options.dump_interval,
                                         dump_out=options.dump_out,
                                         verb_repository=verb_repository,
                                         dump_verb_repo=options.dump_verb_repo,
                                         analyze_lexicons=options.analyze_lexicons,
                                         output_file=output_file)
            
            print "returned sentence count = ",sentence_count
            
            dotest = options.dotest
            if dotest:
                test_out = open(testoutfile,"w")
                print >> test_out,"trained on up to ",input_file," testing on ",test_file
                test_file = open(test_file,"r")
                test(test_file,sem_store,RuleSet,Current_Lex,test_out,sentence_count)
                test_out.close()
            print "at end, lexicon size is ",len(Current_Lex.lex)



def cmd_line_parser():
    """
    Returns the command line parser.
    """
    usage = "usage: %prog [options]\n"
    opt_parser = OptionParser(usage=usage)
    opt_parser.add_option("--min_lex_dump", action="store", type="int", dest="min_lex_dump", default=0,
                          help="the number of iterations before we start dumping lexicons")
    opt_parser.add_option("--max_lex_dump", action="store", type="int", dest="max_lex_dump", default=1000000,
                          help="the number of iterations at which we stop dumping lexicons")
    opt_parser.add_option("-d", action="store_true", dest="dump_lexicons", default=False,
                          help="whether to dump the lexicons or not")
    opt_parser.add_option("--ai", action="store", dest="alternative_input",
                          help="an alternative input file (works only with load_from_pickle)")
    opt_parser.add_option("--dl", action="store", dest="dumped_lexicon",
                          help="a dumped lexicon file (works only with load_from_pickle")
    opt_parser.add_option("--dotest", action="store_true", dest="dotest", default=False,
                          help="use this flag if you want to apply testing")
    opt_parser.add_option("--dinter", action="store", dest="dump_interval", type="int",default=100,
                          help="a dumped lexicon file (works only with load_from_pickle")
    opt_parser.add_option("--dump_out", action="store", dest="dump_out",default='lexicon_dump',
                          help="the prefix for the lexicon dumps")
    opt_parser.add_option("-t", action="store", dest="test_parses",
                          help="the output file for the test parses")
    opt_parser.add_option("-n", action="store", dest="train_parses",
                          help="the output file for the train parses")
    opt_parser.add_option("--dump_vr", action="store_true", dest="dump_verb_repo",default=False,
                          help="whether to dump the verb repository")
    opt_parser.add_option("-i", dest="inp_file",default="trainFiles/trainPairs",
                          help="the input file names (with the annotated corpus)")
    opt_parser.add_option("--analyze", dest="analyze_lexicons",default=False,action="store_true",
                          help="output the results for the experiments")
    
    return opt_parser

if __name__ == '__main__':
    parser = cmd_line_parser()
    options,args = parser.parse_args(sys.argv)
    if len(args) == 1 or args[1] != 'i_n':
        print('Illegal option for now.')
        sys.exit(-1)
    if not options.train_parses or not options.test_parses:
        print('Train and test parses have to be defined')
        sys.exit(-1)
              
    main(args,options)
