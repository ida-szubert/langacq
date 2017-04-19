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
    # expression types which can be returned:
    # constant, predicate, quant, conjunction
    # quant is an expression type for determiners
    # (possesive as well) and quantifiers

    # CHILDES POS tags are:
    #n:prop, n:gerund, n, adj
    #pro:sub, pro:obj, pro:per, pro:poss, pro:rel, pro:refl, pro:exist, pro:int, pro:dem, pro:indef
    #mod:aux, aux, mod, v, part, cop
    #det:dem, det:num, det:poss, det:art
    #adv, adv:int, adv:tem
    #conj, coord, co, prep, post
    #qn

    #n, adj can be like a nominal (one arg, a variable), predicate, or article (if possesive)
    #n:prop can be a constant, predicate, or an article (if possesive)
    #n:gerund can be like a nominal or like a predicate
    #pro:exist has one arg (event)
    #pro:int can be a constant, a placeholder for a nominal, or a predicate (anything really)
    #pro:dem can be a constant or a determiner (2 args)
    #pro:indef can be a constant, a placeholder for a nominal, or a predicate
    #mod:aux, aux, mod are a predicate (2 args, a predicate expression and an event)
    #v, part are a predicate with max 4 arguments (one event and the rest can be e or <ev, t>)
    #cop is like any other verb (if it was parsed as a copula, it wouldn't show up)
    #det:dem is constant or like an article
    #det:num predicate with one arg (nominal or variable(if standing in for a nominal)), constant
    #det:poss should be like articles, some constants due to POS mistakes
    #det:art like article, first arg a variable/constant
    #adv has one argument (variable or predicate)
    #adv:int, adv:tem have one argument (variable)
    #conj has 2 args (predicates)
    #coord has 2 args (can be anything)
    #co is mostly adjunct (one arg, the event), but can be a constant or a predicate
    #prep mostly has 2 args (nominal and event variable), but can have one of them
    #post has one arg (constant, lambda expression, predicate, variable)
    #qn is like an article or adjective

    name = predString.strip().rstrip()
    type = name.split("|")[0]
    # e = None
    args, expString = extractArguments(expString, vardict)
    argTypes = [x.type() for x in args]
    numArgs = len(args)

    #constants or variables
    if numArgs == 0:
        # pro:sub, pro:obj, pro:per (mostly), pro:refl
        # pro:rel (unless used as complementizers or mistaken with det:dem)
        # some tokens of: pro:int, pro:dem, pro:indef, det:dem, det:num, co
        e = constant(name,numArgs,argTypes,type)
        e.makeCompNameSet()
    elif numArgs == 1:
        # adj, n, n:gerund, n:prop, pro:indef,
        # det:num, pro:exist, pro:int, v, part,
        # adv, adv:int, adv:tem, co, prep, post, qn
        e = predicate(name,numArgs,argTypes,type)
        if type in ['adj', 'n', 'n:gerund', 'n:prop', 'pro:indef', 'qn']:
            e.setNounMod()
    elif numArgs == 2:
        # adj, n, n:prop, pro:int, pro:indef, prep
        # mod:aux, aux, mod, v, part, cop, co, n:gerund
        # pro:dem, det:dem, det:poss, det:art, qn
        # conj, coord
        if type in ['pro:dem', 'det:dem', 'det:poss', 'det:art', 'qn']:
            e = quant(name,type,args[0])
            args = args[1:]
        elif type in ['conj', 'coord']:
            e = conjunction()
            e.setType(name)
        else:
            e = predicate(name,numArgs,argTypes,type)
    else:
        # adj, n, pro:indef, pro:int, n:prop
        # v, part, cop, co, n:gerund
        e = predicate(name,numArgs,argTypes,type)

    for i, arg in enumerate(args):
        e.setArg(i,arg)
    e.setString()

    return e, expString

    # # nouns and adjectives can be non-predicative or predicative
    # if type in ["adj","n"]:
    #     numArgs = 1
    #     argTypes = ["e"]
    #     e = predicate(name,numArgs,argTypes,type)
    #     e.setNounMod()
    #     ##e.hasEvent()
    #     # nouns have event markers???
    #     # and adjectives???
    #
    # # IDA: not used
    # elif name == "PAST":
    #     numArgs = 1
    #     argTypes = ["t"]
    #     e = predicate(name,numArgs,argTypes,type)
    #
    # #entities
    # elif type in ["pro","pro:indef","pro:poss","pro:refl","n:prop","pro:dem","pro:wh"]:
    #     numArgs = 0
    #     argTypes = []
    #     e = constant(name,numArgs,argTypes,type)
    #     e.makeCompNameSet()
    #
    # # verb modifiers
    # elif type in ["inf","adv","adv:int","adv:loc","adv:tem"]:
    #     numArgs = 1
    #     argTypes = ["t"]
    #     e = predicate(name,numArgs,argTypes,type)
    #     #e.hasEvent() # think we're dropping out inf though
    #     # events?? - sure thing
    #
    # # introduce lambda
    # elif type in ["det","pro:poss:det","det:num","qn"]:
    #     numArgs = 1
    #     argTypes = ["<e,t>"] # should actually be <e,t>
    #     # return an entity
    #     e = quant(name,type,variable(None))
    #
    # elif type in ["aux"]:
    #     #numArgs = 2
    #     #argTypes = ["subj","action"]
    #     numArgs = 2
    #     argTypes = ["action","event"]
    #     e = predicate(name,numArgs,argTypes,type)
    #
    # elif type in ["adv:wh","pro:wh","det:wh"]:
    #     # obviously don't want to add anything
    #     # for the wh word apart from a lambda term.
    #     # the type of the variable is going to depend
    #     # on the wh word (loc, or otherwise);/../
    #     pass
    #
    # elif type in ["v","part"]:
    #     # whole verbal hierarchy needed here
    #     # do this from a different file
    #     # these are obviously all events
    #     pass
    #
    # elif type in ["conj:coo"]:
    #     e = conjunction()
    #     e.setType(name)
    #
    # elif type in ["prep"]:
    #     numArgs = 2
    #     argTypes = ["e","ev"]
    #     e = predicate(name,numArgs,argTypes,type)
    #     #e.hasEvent()
    # return e, expString


def makeExpWithArgs(expString,vardict):
    print "making ",expString
    is_lambda = expString[:6]=="lambda"
    arguments_present = -1<expString.find("(")<expString.find(")")
    no_commas = expString.find(",")==-1
    commas_inside_parens = -1<expString.find("(")<expString.find(",")

    if is_lambda:
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
        predstring, expString = expString.split("(",1)
        e, expString = makeLogExp(predstring,expString,vardict)
        if e:
            return e, expString
        else:
            e, expString = makeVerbs(predstring,expString,vardict)
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
    else:
        if expString.__contains__(",") and expString.__contains__(")"):
            constend = min(expString.find(","),expString.find(")"))
        else:
            constend = max(expString.find(","),expString.find(")"))
        if constend == -1:
            constend = len(expString)
        conststring = expString[:constend]
        if conststring[0]=="$":
            e, expString = makeVars(conststring, expString[constend:], vardict, parse_args=False)
            # if not vardict.has_key(conststring):
            #     error("unbound var "+conststring)
            # e = vardict[conststring]
            # expString=expString[constend:]
        else:
            e, expString = makeExp(conststring, "", vardict)
    return e,expString


def extractArguments(expString, vardict):
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
                if not a:
                    error("cannot make exp for "+expString[j:i])
                arglist.append(a)
            j = i+1
            if expString[i]==")": finished = True

        elif expString[i]=="(": numBrack+=1
        elif expString[i]==")": numBrack-=1
        i += 1
    return arglist, expString[i:]

# finished = False
# numBrack = 1
# i = 0
# j = 0
# args = []
# while not finished:
#     if numBrack==0:
#         finished = True
#     elif expString[i] in [",",")"] and numBrack==1:
#         a, _ = makeExpWithArgs(expString[j:i],vardict)
#         if not a:
#             error("cannot make exp for "+expString[j:i])
#         e.addArg(a)
#         j = i+1
#         if expString[i]==")": finished = True
#
#     elif expString[i]=="(": numBrack+=1
#     elif expString[i]==")": numBrack-=1
#     i += 1


def makeVars(predstring,expString,vardict,parse_args=True):
    if not vardict.has_key(predstring):
        if "_{" in predstring:
            vname = predstring[:predstring.find("_{")]
            tstring = predstring[predstring.find("_{")+2:predstring.find("}")]
        else:
            vname = predstring
            tstring = 'e'
        t = semType.makeType(tstring)
        e = variable(None)
        e.t = t
        vardict[vname] = e
    else:
        e = vardict[predstring]

    if e.numArgs == 0 and parse_args:
        args, expString = extractArguments(expString, vardict)
        for arg in args:
            e.addArg(arg)
    return e, expString


def makeVerbs(predstring,expString,vardict):
    if predstring.split("|")[0] not in ["v","part"]:
        return None, expString
    args, expString = extractArguments(expString, vardict)
    argTypes = [x.type() for x in args]
    numArgs = len(args)
    verb = predicate(predstring,numArgs,argTypes,predstring.split("|")[0])
    for i, arg in enumerate(args):
        verb.setArg(i,arg)
    verb.setString()
    return verb,expString


# this makes the set logical expressions
def makeLogExp(predstring,expString,vardict):
    e = None
    # adjunctive 'and' takes 2 arguments
    if predstring=="and" or predstring=="and_comp":
        e = conjunction()
        args, expString = extractArguments(expString, vardict)
        for a in args:
            e.addArg(a)
        # finished = False
        # numBrack = 1
        # i = 0
        # j = 0
        # args = []
        # while not finished:
        #     if numBrack==0: finished = True
        #
        #     elif expString[i] in [",",")"] and numBrack==1:
        #         a, _ = makeExpWithArgs(expString[j:i],vardict)
        #         # if r: a = r[0]
        #         # else: error("cannot make exp for "+expString[j:i])
        #         if not a:
        #             error("cannot make exp for "+expString[j:i])
        #         e.addArg(a)
        #         j = i+1
        #         if expString[i]==")": finished = True
        #
        #     elif expString[i]=="(": numBrack+=1
        #     elif expString[i]==")": numBrack-=1
        #     i += 1
        # expString = expString[i:]
        e.setString()

    # IDA: not used any more
    # elif predstring=="eq":
    #     eqargs = []
    #     while expString[0]!=")":
    #         if expString[0]==",": expString = expString[1:]
    #         r = makeExpWithArgs(expString,vardict)
    #         eqargs.append(r[0])
    #         expString = r[1]
    #         #i+=1
    #     if len(eqargs)!=3: error(str(len(eqargs))+"args for eq")
    #     else: e = eq(eqargs[0],eqargs[1],eqargs[2])
    #     expString = expString[1:]
    #     e.setString()
    #     # return (e,expString)
    # 'not' takes 2 arguments, negated expression and event variable
    # IDA: but negation need not be over an event predicate
    elif predstring=="not":
        negargs = []
        while expString[0]!=")":
            if expString[0]==",":
                expString = expString[1:]
            a, expString = makeExpWithArgs(expString,vardict)
            negargs.append(a)
        # if len(negargs)!=2:
        #     error(str(len(negargs))+"args for neg")
        else:
            e = neg(negargs[0], len(negargs))
            if len(negargs) > 1:
                e.setEvent(negargs[1])
        expString = expString[1:]
        e.setString()

    # IDA: Q takes just 1 argument
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

    return e,expString