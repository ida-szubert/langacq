# new translate dependencies. draws more from the pos tags than before
# but still need dependency labels.
from errorFunct import error
from exp import *
# from variable import *
from eventSkolem import *
from lambdaExp import *
from neg import *
from function import *
from conjunction import *
from constant import *
from predicate import *
from eq import *
# from emptyExp import *
from eventMarker import *
import expFunctions


import semType

def findVarIntro(node):
    vI = None
    det = None
    otherqn = None
    vIp = []
    for c in node.children:
        if c.pos in ["pro:poss:det", "det", "qn"]:
            vIp.append(c)
            if c.pos in  ["pro:poss:det", "det"]:
                det = c
            if c.name == "qn|other":
                otherqn = c
                
    if len(vIp)==1:
        c = vIp[0]
        print "qn name is ",c.name
        if vI: return None
        vI = c
        node.remove_child(c)
    elif len(vIp)==2 and det and otherqn:
        qs = det.semTemp
        qs.setArg(1,otherqn.semTemp)
        qs.doubleQuant = True
        det.semTemp = qs
        vI = det
    return vI

def findNounAdjConj(node):
    # also prep in here - bit of apple
    v = variable(None)
    n = node.semTemp
    #print "n is ",node.name
    n.setArg(0,v)
    if len(node.children)==0: 
        print "zero children, returning ",n.toString(True)
        return (n,v)
    e = conjunction()
    gotMod = False
    for c in node.children:
        if len(c.children)==0:
            arg = c.semTemp
            if arg and (not isinstance(arg,list)): print "checking if ",arg.toString(True)," is noun mod"
            if arg and (not isinstance(arg,list)) and arg.isNounMod() and arg.numArgs == 1: 
                arg.setArg(0,v)
                e.addArg(arg)
                gotMod = True
            print "made noun thing ",e.toString(True)
            #elif not arg: print "not arg"
            #elif arg.numArgs!=1: print "numArgs not 1"
            #else: print "is noun mod == ",arg.isNounMod()
        #elif c.name=="prep|of": 
            ## this is WRONG - deal with using events
            #if c.num_children==1 and c.children[0].pos=="n":
                #arg=c.children[0].semTemp
                #print "setting arg in ",arg.toString(True)
                #arg.setArg(0,v)
                #e.addArg(arg)
    if not gotMod:
        return (n,v)
        
        
    e.addArg(n)
    
    #print "
    if len(e.arguments)==1:
        e = e.arguments[0]
    return (e,v)
    
def doNeg(root_sem):
    for node in root_sem.all_nodes():
        if node.pos=="neg":
            # negation should also have an event out front
            # but shouldn't bind it!!!
            if not node.num_parents==1:
                print "not one parent"
                continue 
            if not node.parents[0].semTemp:
                print "not sem for parent"
                continue
            rep = node.parents[0].semTemp
            repo = rep
            if not rep.__class__ in [eventSkolem,lambdaExp]:
                print "neg rep is ",rep.toString(True)
                print rep.__class__
                functrep = rep
                rep.clearParents2()
                functev = variable(None)
                functev.setType(semType.semType.event)
            else:
                functrep = rep.getFunct()
                functrep.remove_parent(rep)
                functev = rep.getVar()
            functrep.clearParents2()
            #print "clearing parents for ",
            print "functrep is ",functrep.toString(True)
            n = neg(functrep)
            
            print "neg is ",n.toString(True)
            n.setArg(1,functev)
            print "neg is ",n.toString(True)
            rep = lambdaExp()
            rep.setVar(functev)
            rep.setFunct(n)
            node.semTemp = n
            for n2 in root_sem.all_nodes():
                if n2.semTemp==repo: n2.semTemp = n


def doPoss(root_sem):
    for node in root_sem.all_nodes():
        
        if node.pos in ["poss","poss|s"] and node.parents!=[] and node.parents[0].pos=="n":
            #if not node.semTemp: print "null sem for ",node.to_string()
            print "poss thing is ",node.parents[0].to_string()
            poss = function("poss",3,["e","<e,t>","e"],"poss")
            ent = None
            for c in node.parents[0].children:
                if c.semTemp and isinstance(c.semTemp,exp) and c.semTemp.isEntity():
                    if ent: continue
                    ent = c.semTemp
            if not ent: continue
            
            nSem = node.parents[0].semTemp
            print "nSem is ",nSem.toString(True)
            newN = nSem.copy()
            #newN = nSem
            #l = exp.lambdaExp()
            v = variable(None)
            poss.setArg(0,v)
            #l.setVar(v)
            newN.setArg(0,v)
            print "newN is ",newN.toString(True)
            #l.setFunct(newN)
            poss.setArg(1,newN)
            poss.setArg(2,ent)
            print "made poss ",poss.toString(True)
            for p in nSem.parents:
                p.replace(nSem,poss)
            poss.argSet=True
            node.parents[0].semTemp = poss
            print "made poss ",poss.toString(True)
        elif node.pos=="poss" and node.parents!=[]: print "parent is ",node.parents[0].to_string()
            # most of these are going to be copula - Mommy's is hot
            # it's baby sarah's



            
def isEq(node):
    pro1=None
    pro2=None
    for c in node.children:
        if c.semTemp and c.semTemp.isEntity():
            if not pro1: pro1=c.semTemp
            elif pro2: 
                print "more than 2 pronouns for cop"
                return None
            else: pro2=c.semTemp
                
        #elif c.cat!="PUNCT":
            #print "false cos of other"
            #return None
        # do we need this objection
    if not pro2: return None
    return (pro1,pro2)

def isET(node):
    # want to find up to one child that is an 
    # entity (or a wh) and up to one child that
    # has category <e,t>
    const = None
    pred = None
    for c in node.children:
        if not c.semTemp: continue
        # look for constant
        if c.semTemp.isEntity():
            if const: return None
            const = c.semTemp
        if c.semTemp.isNounMod():# and \
            #not c.name=="qn|other" and \
            #not c.semTemp.posType=="pro:indef":
            if pred: return None 
            pred = c.semTemp
    if not const: return None
    if not pred: return None
    return (pred,const)
        
#def addNominalisedArgs(root_sem):
    #for node in root_sem.all_nodes():
        #if node.pos in ["v","part"] and node.semTemp:
            #print "semtemp is ",node.semTemp.toString(True)
            #print "is ",node.semTemp
            #if node.semTemp.missingArg(0):
                #pass
            #elif node.semTemp.missingArg(1):
                #print "no Obj"
                #pass
            #elif node.semTemp.missingArg(2):
                #print "no Obj2"
                #pass
        #pass    

def makeConstConj(constList):
    conjSem = conjunction()
    for e in constList:
        conjSem.addArg(e)
    return conjSem

def makeVerbConj(verbList):
    if len(verbList)==1: return None
    # find subj
    # find obj???
    # find ind obj???
    
    
    subjs = []
    objs = []
    indobjs = []
    for v in verbList:
        vNode = v[1]
        vset = v[0]
        obj = getObj(vNode)
        obj2 = getObj2(vNode)
        subj = getSubj(vNode)
        if obj: objs.append(obj)
        if subj: subjs.append(subj)
        if obj2: indobjs.append(obj2)

    failed = False
    vSems = []
    print "SUBJ: ",subjs
    if len(subjs)>1:
        failed = True 
        if len(subjs)!=len(verbList):
            print "funny number of subjects"
        else:
            # make the frickin verbs independently then 
            # conjoin
            pass
    else:
        if len(subjs)>0:
            subj = subjs[0]
        else: subj = None
        for v in verbList:
            vset = v[0]
            vNode = v[1]
            obj = getObj(vNode)
            obj2 = getObj2(vNode)
            vSem = fillOutVerb(vset,subj,obj,obj2)
            vSems.append(vSem)
            
    if not failed: return vSems
    else: return None
        
        
    print "OBJ: ",objs
    if len(objs)>1: print "more than one obj"
    
    print "INDOBJ: ",indobjs
    if len(indobjs)>1: print "more than one indobj"
    # ignore this case

    
def findConjunctions(root_sem):
    for node in root_sem.all_nodes():
        if node.pos=="conj:coo":
            subj = None
            for c in node.children:
                if c.cat=="SUBJ": 
                    if subj: error("two subjs for conj")
                    if c.semTemp: subj = c.semTemp
                    
            if subj: print "gotSubj"

            verbs=True
            verbList = []
            constList = []
            predList = []
            # verbs
            nodeCounter = 0
            for c in node.children:
                if c.cat!="PUNCT":
                    nodeCounter += 1
                    if isinstance(c.semTemp,list):
                        print "verblist ",c.semTemp
                        verbList.append((c.semTemp,c))
                    elif isinstance(c.semTemp,constant):
                        constList.append(c.semTemp)
                    elif isinstance(c.semTemp,predicate):
                        if c.semTemp.isEntity():
                            constList.append(c.semTemp)
                        else: predList.append(c.semTemp)
                    else: print c.semTemp,c.pos," not verblist"

            conjSem = None
            if len(constList)==nodeCounter:
                print "all consts"
                conjSem = makeConstConj(constList)
                for p in node.semTemp.parents:
                    p.replace(node.semTemp,conjSem)
                node.semTemp = conjSem
                conjSem.printOut(True,0)

            elif len(verbList)==nodeCounter:
                print "all verbs ",verbList
                vSems = makeVerbConj(verbList)
                if not vSems: continue
                conjSem = conjunction()
                conjSem.setType(node.name)
                i=0
                for v in vSems:
                    vNode = verbList[i][1]
                    vNode.semTemp = v
                    vNode.setSemDone()
                    i+=1
                    conjSem.addArg(v)
                for p in node.semTemp.parents:
                    p.replace(node.semTemp,conjSem)
                node.semTemp = conjSem
                print "made verb conj ",
                conjSem.printOut(True,0)
                # send the verblist to the function that sorts out
                # verbs. need to share subj but what about obj too?
            elif len(verbList)==nodeCounter-1 and subj and nodeCounter>1:
                print "all verbs and conj has subj"
                
            elif len(predList)==nodeCounter:
                print "all preds"
            else:
                print "????"
            if not conjSem:
                error("conjunction not dealt with "+node.to_string())
            # also got predicates - often attached wrong (attached to 
            # conjunction but they shouldn't be.

#def doConjunctions(root_sem):
    #for node in root_sem.all_nodes():
        #if node.pos=="conj:coo":
            #subj = None
            #for c in node.children:
                #if c.cat=="SUBJ": 
                    #if subj: error("two subjs for conj")
                    #if c.semTemp: subj = c.semTemp
            
            ## entities
            ##for c in node.children
            
            #verbs=True
            #verbList = []
            ## verbs
            #for c in node.children:
                #if c.cat!="PUNCT":# and c.semTemp:
                    ##print c.semTemp
                    #if not c.semTemp or (not c.semTemp.checkIfVerb()): 
                        ##print "here"
                        #verbs = False
                    #else:
                        ##print "here 2" 
                        #verbList.append(c.semTemp)
            
            #subj = None
            #obj = None
            #if not verbs: continue
            #for v in verbList:
                #if v.hasFilledArg(0): subj=v.arguments[0]
                #if v.hasFilledArg(1): obj=v.arguments[1]
            
            #for v in verbList:
                #if v.missingArg(0): pass #subj=v.arguments(0)    
                #if v.missingArg(1): pass #obj=v.arguments(1)
            
            #conj = exp.conjunction()
            #for v in verbList:
                #conj.addArg(v.top_node())
            #node.semTemp = conj
            #print "made conj ",conj.toString(True)
            ##for c in node.children:
                ##if c.semTemp and c.semTemp.checkIfVerb():
                    ##c.semTemp = conj
                    
def doCopula(root_sem):
    for node in root_sem.all_nodes():
        if node.pos=="v:cop":
            # special case intrans v, adj, n
            pc = isET(node)
            if pc:
                # i'm sure  :  eq(I,0) ^ sure(0)
                # eq(ev,sure(I))
                ##error("funny cop")
                # this has real issues with typing
                pred = pc[0]
                const = pc[1]
                print "pred is ",pred.toString(True)
                pred.setArg(0,const)
                print "got cop : ",pred.toString(True)
                node.semTemp=pred
                pass
            
            # special case eq - 2 pronouns    
            nodeArgs = isEq(node)
            if nodeArgs:
                print node.to_string()+" is equal"    
                eqevent = variable(None)
                eqevent.setType(semType.semType.event)
                #eq = exp.eq(nodeArgs[0],nodeArgs[1])
                eq = lambdaExp()
                eq.setVar(eqevent)
                eq.setFunct(eq(nodeArgs[0],nodeArgs[1],eqevent))
                #for p in node.semTemp.parents:
                    #p.replace(node.semTemp,eq)
                print "got cop : ",eq.toString(True)
                node.semTemp = eq
            # special case where
def getNestedAd(adsemnode):
    adsem = adsemnode.semTemp        
    for node in adsemnode.children:
        if node.pos in ["adv","adv:int","adv:loc","adv:tem"] and node.num_parents==1:
            ad = node.semTemp
            ad.setArg(0,adsem.getArg(0))            
            ad = getNestedAd(node)

            c = conjunction()
            c.addArg(adsem)
            c.addArg(ad)
            print "done nested"
            adsem = c
    adsemnode.semTemp = adsem
    print "nested ad is ",adsem.toString(True)
    return adsem

def attachPreds(root_sem):
    for node in root_sem.all_nodes():
        if node.semTemp is None: continue
        if node.pos in ["adv","adv:int","adv:loc","adv:tem"]  and node.num_parents==1 and \
                (node.parents[0].pos in ["v","part"] or node.semTemp.isConjV()):
            ad = node.semTemp
            v = node.parents[0].semTemp
            if not v: 
                print "null semantics for ",node.parents[0].to_string()
                continue
            if not v.getEvent(): 
                error('adv:nullevent')
            else:
                ad.setArg(0,v.getEvent())
                ad = getNestedAd(node)

            c = conjunction()
            print "v is ",v.toString(True)
            c.addArg(v.getFunct())
            c.addArg(ad)
            v.setFunct(c)
            print "v with adv is ",v.toString(True)
            node.parents[0].semTemp=v
            
        #  this is just in case it is a one word sentence 
        elif node.pos in ["adv","adv:int","adv:loc","adv:tem","prep" ]and node.num_parents==0:
            ad = node.semTemp
            print "ad is ",node.semTemp.toString(True)
            node.semTemp = addEvent(ad)
        
        elif node.pos=="prep" and node.num_parents==1:
            # interested in parent mainly
            # attach to verb
            if node.parents[0].pos in ["v","part"]:
                p = node.semTemp
                v = node.parents[0].semTemp
                
                if not v: 
                    print "null semantics for ",node.parents[0].to_string()
                    continue
                
                
                print "doing prep, v is ",v.toString(True)
                #print 'v should have event ',v.toString(True)
                if not v.getEvent(): 
                    error('prep:nullevent')
                else:
                    p.setArg(1,v.getEvent())
                tooManyChildren=False
                adv = []
                for a in node.children:
                    if a.pos in ["n","pro:dem","pro","n:prop","pro:indef"]: # others???
                        if not p.arguments[0].isEmpty():
                            tooManyChildren=True
                            error("more than one arg for "+node.to_string())
                        else:
                            p.setArg(0,a.semTemp)
                    elif a.pos in ["adv","adv:int","adv:loc","adv:tem"]: # others???
                        if a.semTemp is None:
                            print "null sem for ",a.name
                            continue
                        print "got adv ",a.semTemp.toString(True)
                        print "p is ",p.toString(True)
                        a.semTemp.setArg(0,v.getEvent())
                        adv.append(a.semTemp) 

                        #if not p.arguments[0].isEmpty():
                        #    tooManyChildren=True
                        #    error("more than one arg for "+node.to_string())
                        #else:
                        #    p.setArg(0,a.semTemp)

                        pass
                if tooManyChildren:
                    node.semTemp = emptyExp()
                    continue
                
                c = conjunction()
                c.addArg(v.getFunct())
                c.addArg(p)
                for ad in adv:
                    c.addArg(ad)
                v.setFunct(c)
                #print "THIS HAS ",len(v.parents)," PARENTS"
                #if len(v.parents)>1: 
                    #for p in v.parents:
                        #print p.toString(True)
                    #error("too many parents");
                #for parent in v.parents:
                    #if parent.__class__==exp.conjunction:
                        #parent.addArg(p)
                    #else: parent.replace(v,c)
                #infSem.setEvent(vSem.getEvent())
                #print "replacing "+v.toString(True)+" with",
                #c.addArg(v)
                #c.addArg(p)
                print "verb with pred is ",v.toString(True)
                #print c.toString(True)
                #c.setEvent(v.getEvent())
                node.parents[0].semTemp=v
                #print "made prep conj "+c.toString(True)
            # attach to noun
            elif node.parents[0].pos in ["n"]:
                pass
            else:
                print "prep parent is ",node.parents[0].pos#to_string()
                # can be v:cop, adj, conj:coo, adv
                # also pro:indef and det and pro:wh
            # what else can be an event?
            if node.num_children>1:
                print "more than one child for ",node.to_string()
            elif node.num_children==1:
                print "prep has child ",node.children[0].pos
            print 'dealt with prep ',node.semTemp.toString(True)

            #print 'parent is now ',
        pass
    pass    

def attachAdv(root_sem):
    return

#def buildConjunctions(root_sem):
    #for node in root_sem.all_nodes():
        #if node.pos=="conj:coo":
            #pass
            ## find 2, equivalent phrases
            ## share subj, and possibly obj and possibly pred???
    #pass

def buildCompoundNoun(node):
    compSet = []
    for c in node.children:
        if c.pos=="n:prop":
            compSet.append(c)
            compSet.extend(buildCompoundNoun(c))
    return compSet
    
def makeCompoundNouns(root_sem):
    # this only works on proper nouns (mostly Mr Fraser)
    for node in root_sem.all_nodes():
        if node.pos=="n:prop" and node.num_children>0:
            
            #if not isinstance(node.semTemp,exp.constant):
                #print "not constant for ",node.semTemp.toString(True)
            #print "got n:prop with kids for ",node.to_string()
            compSet = buildCompoundNoun(node)
            
            for c in compSet: node.semTemp.addCompName(c.name)
            #if node.name!=node.semTemp.name:
                #print "compound name ",node.semTemp.name

                    


def translateNounMods(root_sem):
    # noun modifiers are hung off nouns.
    # may be     : qn, det - move to front
    #             : adj - conjoin
    #            : other nouns - conjoin
    for node in root_sem.all_nodes():
        if node.pos == "n":
            if node.num_parents==1 and node.parents[0].pos=="n": continue
            #print "got n for ",node.name," parent is ",semantics[node.parents[0]].name
            (argConj,argVar) = findNounAdjConj(node)
            #lTerm = findVarIntro(node)
            quantNode = findVarIntro(node)
            if quantNode:
                quantSem = quantNode.semTemp
                if quantSem.doubleQuant and argConj:
                    quantSem.setVar(argVar)
                    quantSem.arguments[0].setArg(0,argConj)
                #lNode = lTerm.semTemp
                elif argConj:
                    #l = exp.lambdaExp()
                    #l.setVar(argVar)
                    #quantSem.
                    quantSem.setVar(argVar)
                    quantSem.setArg(0,argConj)
                    #l.setFunct(argConj)
                    #lNode.setArg(0,l)
                    #node.semTemp = lNode
                    node.semTemp = quantSem
            else:
                pass 
                #print "NO QUANT"
                #l = exp.lambdaExp()
                #l.setVar(argVar)
                #l.setFunct(argConj)
                #node.semTemp = l

def addSkolem(root_sem):
    for node in root_sem.all_nodes():
        # want to do for mass nouns but 
        # what if they're in a conjunction
        if node.pos == "n" and node.semTemp.name.find("n|")==0:
            nSem = node.semTemp
            print 'n sem is ',nSem.toString(True)
            var = node.semTemp.arguments[0]
            print 'var type is ',type(var)
            print var.__class__
            if var.__class__== emptyExp:
                print 'got empty var'
                continue
            if var.binder is None:
                print 'unbound var in ',nSem.toString(True)
            
            
        pass
        
        
def getObj(node):
    for c in node.children:
        if c.cat=="OBJ": return c.semTemp
    # also could be complement
    #for c in node.children:
        #if c.cat in ["COMP","XCOMP"]: return c.semTemp
    return None
        
def getObj2(node):
    for c in node.children:
        if c.cat in ["OBJ2","IOBJ"]:  return c.semTemp
    return None
        
def getSubj(node):
    for c in node.children:
        if c.cat=="SUBJ":  return c.semTemp
    return None

def setObj(e,e2):
    if e2:
        if e.numArgs<3: 
            error("really only should have obj for trans and ditrans")
            print e.toString(True)
        else:
            e.replace(e.arguments[1],e2)


def setSubj(e,e2):
    if isinstance(e,conjunction):
        for a in e.arguments:
            if a.checkIfVerb: setSubj(a,e2)
        return
    if e2:
        if e.numArgs<2: 
            error("nowhere to put the subject")
        else:
            e.replace(e.arguments[0],e2)
    

def setObj2(e,e2):
    if e2:
        #print "obj2 is ",
        #e2.printOut(True,0)
        if e.numArgs<4: 
            error("really only should have obj2 for ditrans")
        else:
            e.replace(e.arguments[2],e2)

def setAuxVerb(e,e2):
    if e2:
        if e2.__class__==eventSkolem:
            f = e2.funct
            s = e2
            e.replace(e.arguments[0],f)
            e.setArg(1,s.getVar())
            s.setFunct(e)
            return s
        #e.replace(e.arguments[1],e2)
        print "not event ",e2.toString(True)
        #error()
        e.replace(e.arguments[0],e2)
        return e


def fillOutSRL(root_sem):
    for node in root_sem.all_nodes():
        if node.cat=="SRL" and node.semTemp and \
        node.semTemp.__class__==eventSkolem:
            e = node.semTemp.getFunct()
            print "e is ",e.toString(True)
            if node.num_parents==1:
                v=node.parents[0]
                vSem=v.semTemp
                print "vSem is ",vSem.toString(True)
                if vSem.__class__!=eventSkolem:
                    error("Not verb in SRL")
                    return
            c = conjunction()
            
            if node.has_child_cat("SUBJ"):
                subj = node.get_child_cat("SUBJ").semTemp
                vSem.getFunct().setArg(0,subj)
            elif vSem:
                subj = vSem.getFunct().arguments[0]
            
            e.setArg(0,subj)
            e.setEvent(vSem.getEvent())
            c.addArg(e)
            if vSem:
                c.addArg(vSem.getFunct())
                vSem.setFunct(c)
            #for p in v.semTemp.parents:
                #if p!=c: 
                    #if p.__class__==exp.conjunction:
                        #p.addArg(e)
                    #else:
                        #p.replace(v.semTemp,c)
            #v.semTemp=c
            print "got srl conjunction ",v.semTemp.toString(True)
            #v.semTemp.printOut(True,0)
            
def dealWithInf(root_sem):
    for node in root_sem.all_nodes():
        if node.cat=="INF" and node.pos=="inf" and node.semTemp:
            # get subj, gonna be parent of parent
            if node.num_parents==1 and node.parents[0].num_parents==1\
             and node.parents[0].parents[0].semTemp and node.parents[0].semTemp \
             and node.parents[0].parents[0].pos in ["v","part"]:
                print "parentparent is ",node.parents[0].parents[0].semTemp.toString(True)
                subj = node.parents[0].parents[0].semTemp.getFunct().arguments[0]
                print "parentsem ",node.parents[0].semTemp.toString(True)
                if node.parents[0].semTemp.__class__!=eventSkolem:
                    error("not verb in INF")
                    return
                infSem = node.parents[0].semTemp.getFunct()
                
                print "infsem is ",infSem.toString(True)
                vN = node.parents[0].parents[0]
                vSem = vN.semTemp
                if vSem.__class__!=eventSkolem: print "not eventSkolem in inf"
                if infSem: 
                    infSem.setArg(0,subj)
                    infSem.setEvent(vSem.getEvent())
                    if vSem.numArgs>1 and vSem.arguments[1].isEmpty():
                        vSem.setArg(1,infSem)
                    else:
                        c = conjunction()
                        v2 = vSem.getFunct()
                        print "clearning parents for ",v2.toString(True)
                        print "clearning parents for ",infSem.toString(True)
                        infSem.clearParents2()
                        v2.clearParents2()
                        c.addArg(v2)
                        c.addArg(infSem)
                        vSem.setFunct(c)
                        vN.semTemp = vSem
                        print "switching ",node.parents[0].semTemp.toString(True)," with ",vSem.toString(True)
                        node.parents[0].semTemp = vSem
                        node.semTemp = None
                        print "done inf ",vSem.toString(True)
                        #print "this conj is ",c
            else:
                print "inf fail"
    pass    
#def doControlVerbs(root_sem):
    #for node in root_sem.all_nodes(

def addEvent(e):
        event = eventMarker()
        e.setEvent(event)
        sk = eventSkolem()
        sk.setVar(event)
        sk.setFunct(e)
        return sk

def fillOutVerb(verbSemList,subjSem,objSem,indObjSem):
    #error()
    nodeDone=False
    e = None
    for s in verbSemList:
        if s[0]=="c": print "is control"
        if s[0]=="c" or nodeDone: continue
        e = s[1].copy()
        #e.hasEvent()
        print "in fill out verb, e is ",e.toString(True)
        # con,di,t,i in that order
        setObj(e,objSem)
        if objSem: print "adding parent to ",objSem.toString(True)
        setObj2(e,indObjSem)
        if indObjSem: print "adding parent to ",indObjSem.toString(True)
        setSubj(e,subjSem)
        if subjSem: print "adding parent to ",subjSem.toString(True)
        
        e = addEvent(e)
    
        if e.argsFilled(): 
            print "done ",s[0]
            nodeDone = True
        # why was this being done?
        else:
            if objSem:
                print "removing parent2 from ",objSem.toString(True)
                objSem.remove_parent(e)
            if indObjSem: 
                print "removing parent2 from ",indObjSem.toString(True)
                indObjSem.remove_parent(e)
            if subjSem: 
                print "removing parent2 from ",subjSem.toString(True)   
                subjSem.remove_parent(e)
    return e
    
#nullsubj = 0
#def printNullSubj():
    #print nullsubj," null subjects"
    
def fillOutVerbs(root_sem):
    #error()
    # do control verbs separately
    for node in root_sem.all_nodes():
        if node.pos in ["v","part"] and node.semTemp and not node.getSemDone():
            # could be intrans, trans or ditrans
            # some verbs can have multiple templates....
            # see which one fits!!
            nodeDone = False
            e = None
            for s in node.semTemp:
                if s[0]=="c": print "is control"
                if s[0]=="c" or nodeDone: continue
                e = s[1].copy()
                #e.hasEvent()
            
                # con,di,t,i in that order
                obj = getObj(node)
                obj2 = getObj2(node)
                subj = getSubj(node)
                if subj is None and False:#s[0]=="i":
                    subj = expFunctions.makeExp("pro|you")
                    #nullsubj += 1
                #if s[0]=="i":
                    print "nullsubj"
                    root_sem.nullsubj = True
                else:
                    root_sem.nullsubj = False
                    
                setObj(e,obj)
                setObj2(e,obj2)
                setSubj(e,subj)
                
                    
                e = addEvent(e)
                
                
                if e.argsFilled(): 
                    print "done ",s[0]," ",e.toString(True)
                    nodeDone = True
                else:
                    
                    
                    if obj: 
                        print "removing parent1",e.toString(True)," from ",obj.toString(True)," had ",len(obj.parents)," parents"
                        #obj.removeParent(e)
                        obj.clearParents2()
                        print "now has ",len(obj.parents)
                    if obj2: 
                        print "removing parent1 from ",obj2.toString(True)
                        #obj2.removeParent(e)
                        obj2.clearParents2()
                    if subj: 
                        print "removing parent1 from ",subj.toString(True)    
                        #subj.removeParent(e)    
                        subj.clearParents2()
            if e:
                node.semTemp = e
                #print "done verb ",
                e.printOut(True,0)
            else:
                node.semTemp = None
            
def fillOutAux(root_sem):
    # now aux does not take a subject
    for node in root_sem.all_nodes():
        if node.pos == "aux" and node.cat == "AUX" and node.semTemp:
            #print "got aux ",
            e = node.semTemp
            # need to find verb parent
            vSem = None
            subjSem = None
            if node.num_parents==1 and (node.parents[0].pos in ["v","part"]) and node.parents[0].semTemp:
                vSem = node.parents[0].semTemp.top_node()
                #if vSem: vSem = vSem.top_node()
            #if vSem:
                #print "vSem is ",vSem.toString(True)
                #subjSem = vSem.getFunct().arguments[0]
            #setSubj(e,subjSem)
            node.semTemp = setAuxVerb(e,vSem)
            
            #print "aux phrase is"
            #e.printOut(True,0)
            #print "bout to play with aux "
            #node.print_tree2(semantics,"ter",False)
            #p = semantics[node.parents[0]]
            #p.remove_dependent(node.position,semantics)
            #for p2 in p.parents:
                #semantics[p2].remove_dependent(p.position,semantics)
                #semantics[p2].add_dependent(node.position,"?",semantics)
            #node.add_dependent(p.position,"?",semantics)
            #print "played with aux "
            #node.print_tree2(semantics,"ter",False)


def findWhHead(node):
    if node.num_parents==0: return node.semTemp
    if node.num_parents>1: return None
    p = node.parents[0]
    if p.pos in ["v","part"]:
        if p.has_child_cat("AUX"): return p.get_child_cat("AUX").semTemp
        return p.semTemp
    if p.pos == "aux": return p.semTemp
    if p.pos in ["adj","n"]: return p.semTemp
    return None
    
def findWhHead2(semtemp):
    top_node = semtemp.top_node()
    if top_node: print 'top node is ',top_node.toString(True)
    else: print "null top_node"
    #if len(semtemp.parents)==0: return semtemp
    #if len(semtemp.parents)>1: return None
    #p = node.parents[0]
    #if p.pos in ["v","part"]:
        #if p.has_child_cat("AUX"): return p.get_child_cat("AUX").semTemp
        #return p.semTemp
    #if p.pos == "aux": return p.semTemp
    #if p.pos in ["adj","n"]: return p.semTemp
    return top_node
                
def findWh(root_sem,templates):
    # want to know, in place or sentence first???
    
    
    # need to find the argument that the wh refers
    # to and work out where to put the lambda term.
    # how does this work for embedded wh words???
    
    for node in root_sem.all_nodes():
        # need to know if it is at front of sentence or embedded wh
        if node.pos in ["adv:wh","pro:wh"] \
            and node.name.find("why")==-1 \
            and node.name.find("how")==-1 \
            and node.name.find("when")==-1:
                #and node.name.find("where")==-1\
            v = variable(None)
            # what sorts of arguments can these variables
            # fill? only arg in adj, subj or obj or indobj
            # in verb
            if node.parents==[]:
                l = lambdaExp()
                l.setVar(v)
                l.setFunct(v)
                return
                
            p = node.parents[0]
            t = node.cat
            #print "wh type is ",t
            # cannot go by these alone.
            # all of the wh types :
            #    PRED,COM,OBJ,JCT,SUBJ,MOD,POBJ
            
            # PRED - goes with - "what's that" - going with copula 
            #    can also be with "where is ... " though - introduce loc?
            
            # JCT - "why don't ...." go by tag, and introduce Reason(x)
            #  
            
            
            if node.name=="adv:wh|where": 
                print "got where node"
                # where are you going 
                # where is your hat ? 
                # v:cop|be&3S:ROOT(adv:wh|where:PRED , n|hat:SUBJ(pro:poss:det|your:MOD) , ?:PUNCT)
                if p.name=="v:cop|be&3S":
                    asems = []
                    print "got eqloc ",templates["eqLoc"].toString(True)
                    for a in p.children:
                        print "parent has argument ",a.to_string()
                        if a.semTemp:
                            print "this has semTemp ",a.semTemp.toString(True)
                            asems.append(a.semTemp)
                        else: print "no semtemp"
                    if len(asems)==1:
                        v = variable(None)
                        lc = templates["eqLoc"].copy()
                        lc.setArg(0,asems[0])
                        lc.setArg(1,v)
                        lam = lambdaExp()
                        lam.setVar(v)
                        lam.setFunct(lc)
                        p.semTemp = lam
                        #node.semTemp = lam
                        return
                    
                    #print "where cop parent"
                    
                    #print "parent semtemp is ",p.semTemp.toString(True)            
            semtemp = node.semTemp
            if semtemp:
                print 'wh semtemp is ',semtemp.toString(True)
                
            
            
            #if t == "SUBJ" and p.semTemp:
                #p.semTemp.setArg(0,v)
            #if t == "OBJ" and p.semTemp and p.semTemp.numArgs>1:
                #p.semTemp.setArg(1,v)
            #if t == "JCT"  and p.semTemp and p.semTemp.numArgs==1 and p.num_children==1:
                #print "setting arg in ",p.semTemp.toString(True)
                #p.semTemp.setArg(0,v)
                ## this is going to miss a lot of things
                ## like what big red dog -- lx. big(x)^red(x)^dog(x)
                ## in this case we should really treat 'what' like a 
                ## determiner
                e = findWhHead2(semtemp)
                if e: 
                    print 'wh head is ',e.toString(True)
                    l = lambdaExp()
                    l.setFunct(e)
                    e.replace2(semtemp,v)
                    l.setVar(v)
                    print 'wh head with lambda is ',l.toString(True)
                
                
                else: 
                    print 'no wh head'
                    error('no wh head')
                
                
            
            else:
                error('no wh semtemp')
                print 'wh semtemp is ',None
            #if e:
            #l = exp.lambdaExp()
            #l.setFunct(e)
            #l.setVar(v)
                
            #print "got wh ",
            #l.printOut(True,0)
            #else:
                #print "not got wh "
        elif node.name.find("why")!=-1 \
            or node.name.find("where")!=-1\
            or node.name.find("how")!=-1 \
            or node.name.find("when")!=-1:
                error('unusable wh')

                
def splitPast(rep,sentence):
    for st  in rep.allSubExps():
        # need to know if it is at front of sentence or embedded wh
        #if isinstance(node.semTemp,exp.lambdaExp): st = node.semTemp.getDeepFunct()
        #elif isinstance(node.semTemp,exp.eventSkolem): st = node.semTemp.getFunct()
        #else: st = node.semTemp
        print st
        if not st.name: continue
        if st.name.find("-PAST")!=-1:
            pastnode = predicate("PAST",0,"t","PAST")
            st.name=st.name.split("-")[0]
            for p in st.parents:
                print "parent is ",p.toString(True)
                st.remove_parent(p)
                p.replace2(st,pastnode)

            pastnode.setArg(0,st)
            print "made past ",pastnode.toString(True)
            for w in sentence.split():
                if w[-2:]=="ed":
                    print "got match ",w
                    sentence = sentence.replace(w,st.name.split("|")[1]+" ed")

        elif st.name.find("-PERF")!=-1:
            pastnode = predicate("PAST",0,"t","PAST")
            st.name=st.name.split("-")[0]
            for p in st.parents:
                print "parent is ",p.toString(True)
                st.remove_parent(p)
                p.replace2(st,pastnode)

            pastnode.setArg(0,st)
            print "made past ",pastnode.toString(True)
            for w in sentence.split():
                if w[-2:]=="ed":
                    print "got match ",w
                    sentence = sentence.replace(w,st.name.split("|")[1]+" ed")


        if st.name.find("&PAST")!=-1:
            pastnode = predicate("PAST",0,"t","PAST")
            if isinstance(st,conjunction):
                for a in st.arguments:
                    if a.name.find("&PAST")!=-1:
                        st = a
            st.name=st.name.split("&")[0]
            for p in st.parents:
                print "parent is ",p.toString(True)
                st.remove_parent(p)
                p.replace2(st,pastnode)

            pastnode.setArg(0,st)
            print "made past ",pastnode.toString(True)

    return (rep,sentence)
