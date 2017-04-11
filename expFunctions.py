import itertools
from errorFunct import error
from semType import semType
import copy
import random
from tools import permutations
# from variable import *
from predicate import *
from constant import *
from quant import *
from conjunction import *
from lambdaExp import *
from neg import *
from qMarker import *
from eq import *
from exp import *

def parseExp(expString):
    tokens = separate_parens(expString).split()
    expList, _ = parse(tokens, 0)
    return expList


def parse(expression, index):
    # expression can be a lambda expression or a function application
    # returns an expression an the index of the first element after the closing ) of the expression
    if expression[index] == "lambda":
        typed_variable = expression[index+1]
        body, next_index = parse(expression, index+3)
        lam_args = [typed_variable, body]
        return ["lambda", lam_args], next_index+1
    else:
        pred = expression[index]
        args, next_index = parse_arguments(expression, [], index+2)
        return [pred, args], next_index


def parse_arguments(arg_string, args, next_index):
    next_piece = arg_string[next_index]
    if next_piece == ")":
        return args, next_index+1
    elif next_piece != "(":
        if arg_string[next_index+1] != "(":
            args.append(next_piece)
            return parse_arguments(arg_string, args, next_index+1)
        else:
            children_args, new_next_index = parse_arguments(arg_string, [], next_index+2)
            arg = [next_piece, children_args]
            args.append(arg)
            return parse_arguments(arg_string, args, new_next_index)
    else:
        arg, new_next_index = parse(arg_string, next_index)
        args.append(arg)
        return parse_arguments(arg_string, args, new_next_index)


def separate_parens(expression):
    new_expression = []
    for char in expression:
        if char == "(":
            new_expression.append(" ( ")
        elif char == ")":
            new_expression.append(" ) ")
        elif char == ".":
            new_expression.append(" . ")
        elif char == ",":
            new_expression.append(" ")
        else:
            new_expression.append(char)
    return ''.join(new_expression)


def makeExp(predString, expString, vardict):
    name = predString.strip().rstrip()
    type = name.split("|")[0]
    e = None
    # predicates that take a single entity
    if type in ["adj","n"]:
        numArgs = 1
        argTypes = ["e"]
        e = predicate(name,numArgs,argTypes,type)
        e.setNounMod()
        ##e.hasEvent()
        # nouns have event markers???
        # and adjectives???
    # IDA: not used
    elif name == "PAST":
        numArgs = 1
        argTypes = ["t"]
        e = predicate(name,numArgs,argTypes,type)
    #entities
    elif type in ["pro","pro:indef","pro:poss","pro:refl","n:prop","pro:dem","pro:wh"]:
        numArgs = 0
        argTypes = []
        e = constant(name,numArgs,argTypes,type)
        #print "made const for ",name
        e.makeCompNameSet()
    # verb modifiers
    elif type in ["inf","adv","adv:int","adv:loc","adv:tem"]:
        numArgs = 1
        argTypes = ["t"]
        e = predicate(name,numArgs,argTypes,type)
        #e.hasEvent() # think we're dropping out inf though
        # events?? - sure thing

    # introduce lambda
    elif type in ["det","pro:poss:det","det:num","qn"]:
        numArgs = 1
        argTypes = ["<e,t>"] # should actually be <e,t>
        # return an entity
        e = quant(name,type,variable(None))

    elif type in ["aux"]:
        #numArgs = 2
        #argTypes = ["subj","action"]
        numArgs = 2
        argTypes = ["action","event"]
        e = predicate(name,numArgs,argTypes,type)

    elif type in ["adv:wh","pro:wh","det:wh"]:
        # obviously don't want to add anything
        # for the wh word apart from a lambda term.
        # the type of the variable is going to depend
        # on the wh word (loc, or otherwise);/../
        pass
    elif type in ["v","part"]:
        # whole verbal heirarchy needed here, do this
        # from a different file
        # these are obviously all events

        pass
    elif type in ["conj:coo"]:
        # check both sides and then conjoin
        e = conjunction()
        e.setType(name)
        #pass
    elif type in ["prep"]:
        numArgs = 2
        argTypes = ["e","ev"]
        e = predicate(name,numArgs,argTypes,type)
        #e.hasEvent()
    elif type in ["pro:wh"]:
        # WTF
        pass
        # e=emptySem()
    #else:
        #print name,"  ",type
    args, expString = extractArguments(expString, vardict)
    for i, arg in enumerate(args):
        e.setArg(i,arg)
    e.setString()
    return (e, expString)


def makeExpWithArgs(expString,vardict):
    print "making ",expString
    arguments_present = -1<expString.find("(")<expString.find(")")
    no_commas = expString.find(",")==-1
    commas_inside_parens = -1<expString.find("(")<expString.find(",")

    if expString[:6]=="lambda":
        vname = expString[7:expString.find("_{")]
        tstring = expString[expString.find("_{")+2:expString.find("}")]
        t = semType.makeType(tstring)
        v = variable(None)
        v.t = t
        vardict[vname] = v
        expString = expString[expString.find("}.")+2:]
        (f,expString) = makeExpWithArgs(expString,vardict)
        e = lambdaExp()
        e.setFunct(f)
        e.setVar(v)
        e.setString()

    elif arguments_present and (commas_inside_parens or no_commas):
        # predstring = expString.split("(")[0]
        # expString=expString[expString.find("(")+1:]
        predstring, expString = expString.split("(",1)
        e, expString = makeLogExp(predstring,expString,vardict)
        if e:
            return e, expString
        else:
            e, expString = makeVerbs(predstring,expString,vardict)
            # if r:
            #     e=r[0]
            # elif predstring[0]=="$":
            if e is None:
                if predstring[0]=="$":
                    e, expString = makeVars(predstring,expString,vardict)
                else:
                    e, expString = makeExp(predstring, expString, vardict)
                if e is None:
                    print "none e for |" + predstring + "|"
                # IDA: don't know what this is but I messed with expString above
                if e.__class__  == quant:
                    var = e.getVar()
                    var.t = semType.e
                    varname = expString[:expString.find(",")]
                    vardict[varname]=var
                    expString = expString[expString.find(","):]
            # read in the arguments
            # i=0
            # finished = False
            # numBrack = 1
            # i = 0
            # j = 0
            # argcount = 0
            # while not finished:
            #     if numBrack==0:
            #         finished = True
            #     elif expString[i] in [",",")"] and numBrack==1:
            #         if i>j:
            #             r = exp.makeExpWithArgs(expString[j:i],vardict)
            #             if r: a = r[0]
            #             else: error("cannot make exp for "+expString[j:i])
            #             e.setArg(argcount,a)
            #             argcount+=1
            #         j = i+1
            #         if expString[i]==")": finished = True
            #
            #     elif expString[i]=="(": numBrack+=1
            #     elif expString[i]==")": numBrack-=1
            #
            #     i += 1
            # expString = expString[i:]
    # constants
    else:
        if expString.__contains__(",") and expString.__contains__(")"):
            constend = min(expString.find(","),expString.find(")"))
        else:
            constend = max(expString.find(","),expString.find(")"))
        if constend == -1:
            constend = len(expString)
        conststring = expString[:constend]
        if conststring[0]=="$":
            if not vardict.has_key(conststring):
                error("unbound var "+conststring)
            e = vardict[conststring]
            expString=expString[constend:]
        else:
            e, expString = makeExp(conststring, "", vardict)
        # expString=expString[constend:]
        # e.setString()
    return (e,expString)


def extractArguments(expString, vardict):
    i=0
    finished = False if expString else True
    numBrack = 1
    i = 0
    j = 0
    arglist = []
    while not finished:
        if numBrack==0:
            finished = True
        elif expString[i] in [",",")"] and numBrack==1:
            if i>j:
                a, _ = makeExpWithArgs(expString[j:i],vardict)
                # if r: a = r[0]
                # else: error("cannot make exp for "+expString[j:i])
                if not a:
                    error("cannot make exp for "+expString[j:i])
                arglist.append(a)
            j = i+1
            if expString[i]==")": finished = True

        elif expString[i]=="(": numBrack+=1
        elif expString[i]==")": numBrack-=1
        i += 1
    return arglist, expString[i:]


# this gives the vars the arguments that they need
def makeVars(predstring,expString,vardict):
    if not vardict.has_key(predstring):
        error("unbound var "+predstring)
    e = vardict[predstring]
    # numArgs = 1
    # finished = False
    # numBrack = 1
    # i = 0
    # while not finished:
    #     if numBrack==0: finished = True
    #     elif expString[i]=="," and numBrack==1: numArgs += 1
    #     elif expString[i]==")": numBrack-=1
    #     elif expString[i]=="(": numBrack+=1
    #     #elif expString[i]=="," and numBrack==1: numArgs += 1
    #     i += 1
    args, expString = extractArguments(expString, vardict)
    # for i in range(numArgs):
    #     e.addArg(emptyExp())
    for arg in args:
        e.addArg(arg)
    return (e, expString)


# this makes the set verbs
def makeVerbs(predstring,expString,vardict):
    if predstring.split("|")[0] not in ["v","part"]:
        return None, expString
    # numArgs = 1
    # finished = False
    # numBrack = 1
    # i = 0
    # while not finished:
    #     if numBrack==0: finished = True
    #     elif expString[i]=="," and numBrack==1: numArgs += 1
    #     elif expString[i]==")": numBrack-=1
    #     elif expString[i]=="(": numBrack+=1
    #     i += 1
    args, expString = extractArguments(expString)
    # argTypes = []
    # for i in range(numArgs): argTypes.append(semType.e)
    argTypes = [x.type() for x in args]
    numArgs = len(args)
    verb = predicate(predstring,numArgs,argTypes,predstring.split("|")[0])
    for i, arg in enumerate(args):
        verb.setArg(i,arg)
    verb.setString()
    return (verb,expString)


# this makes the set logical expressions
def makeLogExp(predstring,expString,vardict):
    e = None
    if predstring=="and" or predstring=="and_comp":
        e = conjunction()
        finished = False
        numBrack = 1
        i = 0
        j = 0
        args = []
        while not finished:
            if numBrack==0: finished = True

            elif expString[i] in [",",")"] and numBrack==1:
                a, _ = makeExpWithArgs(expString[j:i],vardict)
                # if r: a = r[0]
                # else: error("cannot make exp for "+expString[j:i])
                if not a:
                    error("cannot make exp for "+expString[j:i])
                e.addArg(a)
                j = i+1
                if expString[i]==")": finished = True

            elif expString[i]=="(": numBrack+=1
            elif expString[i]==")": numBrack-=1
            i += 1
        expString = expString[i:]
        e.setString()
        # return (e,expString)

    # need arg1 arg2
    # IDA: not used any more
    elif predstring=="eq":
        eqargs = []
        while expString[0]!=")":
            if expString[0]==",": expString = expString[1:]
            r = makeExpWithArgs(expString,vardict)
            eqargs.append(r[0])
            expString = r[1]
            #i+=1
        if len(eqargs)!=3: error(str(len(eqargs))+"args for eq")
        else: e = eq(eqargs[0],eqargs[1],eqargs[2])
        expString = expString[1:]
        e.setString()
        # return (e,expString)

    elif predstring=="not":
        negargs = []
        while expString[0]!=")":
            if expString[0]==",":
                expString = expString[1:]
            a, expString = makeExpWithArgs(expString,vardict)
            negargs.append(a)
            # expString = r[1]
        if len(negargs)!=2:
            error(str(len(negargs))+"args for neg")
        else:
            e = neg(negargs[0])
            e.setEvent(negargs[1])
        expString = expString[1:]
        e.setString()
        # return (e,expString)
    elif predstring == "Q":
        qargs = []
        while expString[0]!=")":
            if expString[0]==",": expString = expString[1:]
            r = makeExpWithArgs(expString,vardict)
            qargs.append(r[0])
            expString = r[1]
            #i+=1
        if len(qargs)!=1: error(str(len(qargs))+"args for Q")
        else:
            e = qMarker(qargs[0])
            # e.setEvent(qargs[1])

        expString = expString[1:]
        # e.setString()
        # return (e,expString)


    elif predstring == "eqLoc":
        eqargs = []
        while expString[0]!=")":
            if expString[0]==",": expString = expString[1:]
            r = makeExpWithArgs(expString,vardict)
            eqargs.append(r[0])
            expString = r[1]
        if len(eqargs)!=2: error(str(len(eqargs))+"args for eqLoc")
        else:
            e = predicate("eqLoc",2,["e","e"],None)
            e.setArg(0,eqargs[0])
            e.setArg(1,eqargs[1])
        expString = expString[1:]
        e.setString()
        # return (e,expString)
    elif predstring == "evLoc":
        eqargs = []
        while expString[0]!=")":
            if expString[0]==",": expString = expString[1:]
            r = makeExpWithArgs(expString,vardict)
            eqargs.append(r[0])
            expString = r[1]
        if len(eqargs)!=2: error(str(len(eqargs))+"args for evLoc")
        else:
            e = predicate("evLoc",2,["e","ev"],None)
            e.setArg(0,eqargs[0])
            e.setArg(1,eqargs[1])

        expString = expString[1:]
        e.setString()
    return (e,expString)