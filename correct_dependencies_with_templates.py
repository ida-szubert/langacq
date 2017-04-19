from exp import *
from constant import *
from eventMarker import *
# from emptyExp import *
# from variable import *
from qMarker import *
from conjunction import *
from lambdaExp import *
# from oldTranslationFunctions import *
from newTranslationFunctions import *
import readInExps
import sys
import errorFunct
import string
from cat import synCat
from cat import cat
from semType import semType


class sem_node:
    def __init__(self, name, semanticTemplate):
        self.name = name
        self.pos = name.split('|')[0]
        self.cat = None
        self.children = []
        self.parents = []
        self.semTemp = semanticTemplate
        self.num_children = 0
        self.num_parents = 0
        self.semDone = False
        self.position = None
        self.nullsubj = False

    def setPosition(self, position):
        self.position = position

    def setSemDone(self):
        self.semDone = True

    def getSemDone(self):
        return self.semDone

    def set_cat(self, cat):
        self.cat = cat

    def add_child(self, child):
        if not child in self.children:
            self.children.append(child)
            self.num_children += 1
            child.add_parent(self)

    def remove_child(self, child):
        if child in self.children:
            child.remove_parent(self)
            del self.children[self.children.index(child)]
            self.num_children -= 1

    def del_node(self, node):
        # cannot delete root
        self.remove_child(node)
        for c in self.children:
            c.del_node(node)

    def all_nodes2(self, node_set):
        for c in self.children:
            c.all_nodes2(node_set)
        if not self in node_set:
            node_set.append(self)

    def all_nodes(self):
        node_set = []  # set([])
        self.all_nodes2(node_set)
        return node_set

    def add_parent(self, parent):
        if not parent in self.parents:
            self.parents.append(parent)
            self.num_parents += 1

    def remove_parent(self, parent):
        if parent in self.parents:
            del self.parents[self.parents.index(parent)]
            self.num_parents -= 1

    def replaceSemTemp(self, s):
        if not self.semTemp: self.semTemp = s
        for p in self.semTemp.parents:
            p.replace(self.semTemp, s)
        self.semTemp = s

    def replaceEqSemTemp(self, s1, s2):
        if self.semTemp == s1: self.replaceSemTemp(s2)

    def has_child_cat(self, cat):
        for c in self.children:
            if c.cat == cat: return True
        return False

    def get_child_cat(self, cat):
        for c in self.children:
            if c.cat == cat: return c

    def to_string(self):
        s = self.name + ":" + self.cat
        if self.children != []:
            s = s + "("
        for i in range(len(self.children)):
            s = s + self.children[i].to_string()
            if i < len(self.children) - 1:
                s = s + " , "
            else:
                s = s + ")"
        return s

    def print_self(self):
        print self.to_string()
        # def find_loop(self,node_set):


######## DEAL WITH DEPENDENCY LINE ############
# get rid of co| - only if there is only one  #
# these dependencies are only a pointer to    #
# what the correct arguments should be in our #
# semantic templates                          #
###############################################

def x_line(line, semantics, sentence):
    conj = False
    # for node in semantics:
    # if node.name == 'conj:coo|and':
    # print "returning conj:coo"
    # return None

    ##############################
    ## gets original tree        ##
    ##############################
    deps = line[6:].split()
    root_sem = None
    if len(deps) == len(semantics):
        i = 0
        for dep in deps:
            bits = dep.split('|')
            if int(bits[0]) != i + 1:
                print "returning x-line"
                return None
            if int(bits[1]) != 0:
                semantics[int(bits[1]) - 1].add_child(semantics[int(bits[0]) - 1])
                semantics[int(bits[0]) - 1].set_cat(bits[2])

            if dep.find('ROOT') != -1:
                semantics[i].set_cat(bits[2])
                root_sem = semantics[i]
            i = i + 1

        return root_sem
    else:
        print sentence
        print semantics
        print deps
        print 'not same length ', len(deps), ' ', len(semantics)
        return None

        ################################
        ## put some structure in here ##
        ################################


def translateGraph(root_sem, templates):
    # at the moment, partialCompletions is not being used at all.
    # in fact, neither are the templates

    # doConjunctions(root_sem) # here??


    makeCompoundNouns(root_sem)
    translateNounMods(root_sem)
    doPoss(root_sem)

    # function to find out if variable is bound
    # really want det introducing variable

    # name skolem, initially for mass nouns but maybe also for 
    #     places
    #     
    # addSkolem(root_sem)

    # find conjunctions of verbs and nouns
    conjunctions = findConjunctions(root_sem)

    fillOutVerbs(root_sem)
    dealWithInf(root_sem)
    fillOutSRL(root_sem)

    fillOutAux(root_sem)
    # maybe can deal with this problem using skolem
    # terms!!!
    attachPreds(root_sem)
    doCopula(root_sem)  # here???

    # addNominalisedArgs(root_sem)
    doNeg(root_sem)

    findWh(root_sem, templates)
    # doWhQ(root_sem)

    return root_sem


def cleanVocAndCom(sentence, sem_list, root_sem):
    # this will only strip of the front and back
    # VOC and COM entries. 
    # print "sentence si ", sentence
    words = sentence.split()
    fromFront = False

    if sem_list[0].cat in ["COM", "VOC"]:
        root_sem.del_node(sem_list[0])
        del sem_list[0]
        del words[0]
    # print "words are ",words
    if sem_list[-2].cat in ["COM", "VOC"]:
        root_sem.del_node(sem_list[-2])
        del sem_list[-2]
        del words[-2]

    sentence = " ".join(words)

    for s in sem_list:
        if s.cat in ["COM", "VOC"]:
            root_sem = None
            sem_list = None
            sentence = None
            # print "rejecting because of COM or VOC"
    return (sentence, sem_list, root_sem)


def checkForNounDeps(root_sem, sent, semline):
    reps = set([])
    for e in root_sem.all_nodes():
        if e.pos == "n":
            for c in e.children:
                if c.pos not in ["det", ".", "pro:poss:det", "?", "qn", "adj", "poss", "pro:poss:det", "n"]:
                    print "weird mod ", c.pos, sent, root_sem.to_string()
                    return False
    return True


def checkForAdjAdv(root_sem, sent, semline):
    reps = set([])
    for e in root_sem.all_nodes():
        if e.pos == "adj":
            for c in e.children:
                if c.pos in ["adv:int", "adv"]:
                    print "adjAdv ", c.pos, sent, root_sem.to_string()
                    return False
    return True


def getRepFragments(root_sem):
    reps = set([])
    for e in root_sem.all_nodes():
        if e.semTemp and e.semTemp.argSet or e.semTemp.__class__ == constant:
            reps.add(e.semTemp.top_node())
    reps.discard(None)
    todel = []
    for r in reps:
        if r.__class__ == conjunction:
            for r2 in reps:
                if r2.__class__ == conjunction:
                    if set(r.arguments).issubset(r2.arguments):
                        todel.append(r)
    for r in todel:
        reps.discard(r)
    return reps


def getCompleteLine(f, i, line):
    if i == len(f): return line
    if f[i][0] not in ["%", "*", "@"]:
        line = line + " " + f[i].strip().rstrip()
        return getCompleteLine(f, i + 1, line)
    return line


def getVerb(semName, iV, tV, dtV, con):
    semTemp = []
    if con.has_key(semName): semTemp.append(("c", con[semName]))
    if dtV.has_key(semName): semTemp.append(("d", dtV[semName]))
    if tV.has_key(semName): semTemp.append(("t", tV[semName]))
    if iV.has_key(semName): semTemp.append(("i", iV[semName]))
    if semTemp == []: semTemp = None
    if not semTemp and (semName[:2] == "v|" or semName[:5] == "part|"):
        print "no template for ", semName
    return semTemp


def recurseSplit(topCat, i, max, semStore):
    return
    if semStore.has_key(topCat.toString()): return
    if i < max and not isinstance(topCat.getSem(), variable):
        catSplits = topCat.allPairs()
        semStore[topCat.toString()] = catSplits
        for (left, right) in catSplits:
            print left.toString(), " ", right.toString()
            recurseSplit(left, i + 1, max, semStore)
            recurseSplit(right, i + 1, max, semStore)


def checkUnboundVar(rep):
    for e in rep.allSubExps():
        for a in e.arguments:
            # print 'e is ',e.toString(True)
            if a.__class__ == variable or a.__class__ == eventMarker:
                print 'got var'
                if a.binder is None:
                    # pass
                    errorFunct.error('unbound variable in ' + rep.toString(True))


def checkEmpty(rep):
    for e in rep.allSubExps():
        for a in e.arguments:
            if a.__class__ == emptyExp:
                # pass
                errorFunct.error('emptyExp in ' + rep.toString(True))


def collapseFragments(replist):
    todel = []
    for r1 in replist:
        for r2 in replist:
            for e in r2.allSubExps():
                if e == r1 and not e == r2 and not r1 in todel: todel.append(r1)
    for r in todel:
        print 'removing ', r.toString(True)
        replist.remove(r)
    return replist


def checkNonConstDup(rep):
    seensubexps = []
    for e in rep.allSubExps():
        if e in seensubexps and e.__class__ != constant and e.__class__ != variable:
            errorFunct.error("non const duplication " + e.toString(True))
        seensubexps.append(e)


def checkIfWh(rep):
    is_lambda = rep.__class__ == lambdaExp
    if is_lambda:
        has_e_var = rep.getVar().type() == semType.e
        funct = rep.getFunct()
        funct_is_lambda = funct.__class__ == lambdaExp
        if is_lambda and has_e_var and funct_is_lambda:
            return True
    else:
        return False


def repFromExample(line_count, semStore, f, output, ubloutput, rejected, c, w, templates, iV, tV, dtV, con, eveAll,
                   childOutput=None):
    Done = False
    mother = False
    totsentlen = 0
    numsents = 0
    ischild = False
    while not Done and line_count < len(f):
        if f[line_count] in ["", "\n"]:
            line_count += 1
            continue

        line = getCompleteLine(f, line_count + 1, f[line_count].strip().rstrip())
        # print "line_count = ",line_count
        line_count += 1
        if line[:2] == "//": continue
        childOutput = False
        if line[0] == '*' and (childOutput or line[:5] != '*CHI:'):
            ischild = False
            print "trying :: ", line
            if line[:5] == '*CHI:': ischild = True
            if line.find('#') == -1 and line.find(',') == -1 and line.find('+...') == -1 and line.find('xxx') == -1:
                mother = True
                line = line[6:]
                line = line.rstrip()
                line = line.strip()
                line = line.replace("(.) ", "")
                sentence = line
                if sentence == "what ?": error("whatsent")

        elif line[:5] == '%trn:' and mother:
            sem_list = []
            semantic_components1 = []
            semantic_components = line[6:].split()
            for item in semantic_components:
                semantic_components1.extend(item.split('~'))
            semantic_components = []
            for item in semantic_components1:
                if item.find('-POSS') != -1:
                    semantic_components.extend([item.split('-POSS')[0], '-POSS'])
                else:
                    semantic_components.append(item)

            semTemps = []
            # semcompcount = 0
            position = 0
            for item in semantic_components:
                semName = item
                semTemp = None
                if templates.has_key(semName):
                    semTemp = templates[semName].copy()
                else:
                    # might be verb - more than one
                    semTemp = getVerb(semName, iV, tV, dtV, con)
                # semcompcount = semcompcount+1
                node = sem_node(item, semTemp)
                node.setPosition(position)
                sem_list.append(node)
                position += 1

        elif line[:5] == '%grt:' and mother:
            # print "here"
            root_sem = x_line(line, sem_list, sentence)
            if root_sem:
                (sentence, sem_list, root_sem) = cleanVocAndCom(sentence, sem_list, root_sem)
            if root_sem:
                nounwrong = checkForNounDeps(root_sem, sentence, line)
                adjAdvWrong = checkForAdjAdv(root_sem, sentence, line)

                allowedchars = list(string.letters)
                allowedchars.extend(["'", ".", "?", " "])
                disallowed = []
                for c in sentence:
                    if c not in allowedchars: disallowed.append(c)
                for c in disallowed:
                    sentence = sentence.replace(c, "")
                print "\n\nSent: " + sentence
                print "Dep Tree: " + root_sem.to_string() + "\n"

                if not ischild: print >> eveAll, "Sent: ", sentence
                if not ischild: print >> eveAll, "Sem: ", root_sem.to_string() + "\n"

                errorFunct.reset_flag()
                root_sem = translateGraph(root_sem, templates)
                if root_sem and root_sem.nullsubj and ischild: print "nullSubj for ", sentence
                # if not root_sem: print "no root sem for ",sentence

                print "partial reps are::"
                pR = getRepFragments(root_sem)
                for rep in pR:
                    rep.printOut(True, 0)
                    rep.printOut(True, 0)
                    # print 'checking vars'
                    # checkUnboundVar(rep)

                    # print 'done for that rep'
                # this is not good enough, need better error checking, 
                # many things are not properly dealt with
                pR = collapseFragments(pR)
                rep = None
                if len(pR) == 1:
                    rep = pR.pop()
                    checkUnboundVar(rep)
                    checkEmpty(rep)
                    checkNonConstDup(rep)
                else:
                    errorFunct.error('more or fewer than one rep fragment')
                    for r in pR:
                        print r.toString(True)
                        # if len(pR)==2:
                        # if pR[0].pos
                if sentence == "what ?": error("whatsent")
                print "sentence is |" + sentence + "|"
                if not errorFunct.check_flag():
                    if rep.type() is None:
                        error("badly typed rep : " + rep.toString(True))
                    else:
                        sentlen = sentence.count(' ')
                        totsentlen += sentlen
                        numsents += 1
                        words = sentence.split()
                        print 'got good rep: ', rep.printOut(True, 0)
                        if not nounwrong:
                            print "nounwrong but good rep"
                        if not adjAdvWrong:
                            print "adjAdvErr"
                        if checkIfWh(rep):
                            sc = synCat.swh
                        elif words[-1] == "?":
                            if not rep.__class__ in [eventSkolem, lambdaExp]:
                                print "qmarked rep is ", rep.toString(True)
                                print rep.__class__
                                # print rep.getVar().type().equals(semType.event)
                                functrep = rep
                                functev = variable(None)
                                functev.setType(semType.event)
                                # error("q problem")
                            else:
                                functrep = rep.getFunct()
                                functev = rep.getVar()
                                # print
                                print "functrep is ", functrep.toString(True)
                            q = qMarker(functrep)
                            print "q is ", q.toString(True)
                            # q.setArg(0,rep)
                            q.setArg(1, functev)
                            print "q is ", q.toString(True)
                            rep = lambdaExp()
                            rep.setVar(functev)
                            rep.setFunct(q)
                            # rep = q
                            sc = synCat.q
                        else:
                            sc = synCat.allSynCats(rep.type())[0]
                        (rep, sentence) = splitPast(rep, sentence)

                        topcat = cat(sc, rep)
                        sentence = sentence.replace("\'", " \'")
                        sentence = sentence.replace("(", "")
                        sentence = sentence.replace(")", "")
                        print 'topcat is :: ', topcat.toString()

                        if ischild:
                            print >> childOutput, "\n\nSent: " + sentence
                            print >> childOutput, "Sem:  " + rep.toString(True)
                            print >> childOutput, "example_end\n"
                        else:
                            if root_sem and root_sem.nullsubj: print "nullSubjSuccess for ", sentence
                            print >> output, "\n\nSent: " + sentence
                            print >> output, "Sem:  " + rep.toString(True)
                            print >> output, "example_end\n"
                            sentence = sentence.rstrip().rstrip(".").rstrip()
                            sentence = sentence.rstrip().rstrip("?").rstrip()
                            print >> ubloutput, "\n" + sentence
                            print >> ubloutput, rep.toStringUBL(True)

                            # print "\n\nsplitting rep"
                            # print "splits are:"
                            # rep.makePairs()
                            # print >> output,split

                            # for subexp in rep.allSubExps():
                            # print "subexp: ",subexp.toString(True)
                            # for split in rep.makePairs():
                            # print >> output,split

                        # print "\n\nrecursively split ",topCat.toString()
                        # recurseSplit(topCat,1,4,semStore)
                        Done = True
                        return (sentence, topcat, line_count)

                if errorFunct.check_flag():
                    print "ERROR found"
                    if not ischild:
                        print >> rejected, "Sent: ", sentence
                        if root_sem: print >> rejected, "Sem: ", root_sem.to_string(), "\n"
                    if root_sem.nullsubj and not ischild: print "nullsubj rejection ", root_sem.to_string()
                mother = False
                continue
                # if errorFunct.check_flag():
                # print "ERROR found"
            print >> rejected, sentence
            if root_sem: print >> rejected, root_sem.to_string(), "\n"
            mother = False
        elif line[0] == "*":
            # print "here ",line,line_count
            mother = False
    return (None, None, line_count)


def dealWithFile(f, output, c, w, templates, iV, tV, dtV, con, eveAll):
    semStore = {}
    mother = False
    line_count = 0
    totsentlen = 0
    numsents = 0
    while line_count < len(f):
        (sentence, topCat, line_count) = repFromExample(line_count, semStore, f, output, c, w, templates, iV, tV, dtV,
                                                        con, eveAll)
        if topCat:
            totsentlen += sentence.count(' ')
            numsents += 1
            c += 1
        else:
            print "rejected"
            w += 1
    # this should not be here
    # print 'avg sent len = ',float(totsentlen)/numsents
    return (c, w)


def main():
    templates = {}

    # this does the easy things
    inFile = open("/home/tom/Corpora/Brown/Eve/scripts/sems", "r")
    readInExps.addFromFile(inFile, templates)

    # the order in which these are read in is important
    # as we only let each verb live in one of the families
    # and there may be (accidental) duplication in the input.
    iV = {}
    intransVerbs = open("/home/tom/Corpora/Brown/Eve/scripts/intransVerbs", "r")
    readInExps.addIntransVerbs(intransVerbs, iV)

    tV = {}
    transVerbs = open("/home/tom/Corpora/Brown/Eve/scripts/transVerbs", "r")
    readInExps.addTransVerbs(transVerbs, tV)

    dtV = {}
    ditransVerbs = open("/home/tom/Corpora/Brown/Eve/scripts/ditransVerbs", "r")
    readInExps.addDitransVerbs(ditransVerbs, dtV)

    con = {}
    controlVerbs = open("/home/tom/Corpora/Brown/Eve/scripts/controlVerbs", "r")
    readInExps.addDitransVerbs(controlVerbs, con)

    c = 0
    w = 0
    output = open('trainPairs.txt', 'w')
    eveAll = open('eveAll.txt', 'w')
    for i in range(1, 21):
        print "i is ", i
        if i < 10:
            fName = "/home/tom/Corpora/Brown/Eve/eve0" + str(i) + ".cha"
        else:
            fName = "/home/tom/Corpora/Brown/Eve/eve" + str(i) + ".cha"
        print "fName is ", fName
        f = open(fName, "r")
        (c, w) = dealWithFile(f.readlines(), output, c, w, templates, iV, tV, dtV, con, eveAll)
    print c, ' correct sentences.  ', w, ' discarded'

    # vOutFile = open("vFrames","w")
    # argSet = {}
    # verbSet = {}
    # for v in vOut:
    # argKey = v[v.find("("):]
    # if not argSet.has_key(argKey): argSet[argKey]=[v]
    # else: argSet[argKey].append(v)
    # verbKey = v[:v.find("(")]
    # if not verbSet.has_key(verbKey): verbSet[verbKey]=[v]
    # else: verbSet[verbKey].append(v)

    # for a in argSet:
    # print >> vOutFile,"\n\n"+a
    # for v in argSet[a]:
    # print >> vOutFile,v,"  ",vOut[v]

    # print >> vOutFile,"\n\n\n\n"
    # for a in verbSet:
    # print >> vOutFile,"\n\n"+a
    # for v in verbSet[a]:
    # print >> vOutFile,v,"  ",vOut[v]

    # origVOutFile = open("origVFrames","w")
    # for v in origV:
    # print >> origVOutFile,v,"  ",origV[v]

# main()
