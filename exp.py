# expression, on which everything else is built
import itertools
from errorFunct import error
from semType import semType
#from cat import synCat
#from cat import cat
import copy
import random
from tools import permutations
from expFunctions import *

verboseSplit = False
class exp:
    varNum = 0
    eventNum = 0
    emptyNum = 0
    allowTypeRaise = True
    def __init__(self,name,numArgs,argTypes,posType):
        self.onlyinout = None
        self.linkedVar = None
        self.name = name
        self.numArgs = numArgs
        if numArgs!=len(argTypes): 
            print "error, not right number of args"
        self.argTypes = argTypes
        self.arguments = []
        self.parents = []
        for aT in argTypes:
            self.arguments.append(emptyExp())
        self.setReturnType()
        self.functionExp = self
        self.nounMod = False
        self.posType = posType    
        self.argSet = False
        self.isVerb=False
        self.isNull = False
        self.inout = None
        self.doubleQuant = False
        self.string = ""


    def setString(self):
        self.string = self.toString(True)

    def resetBinders(self):
        for e in self.allSubExps():
            if e.__class__ in [lambdaExp,quant]:
                e.var.setBinder(e)

    def repairBinding(self, orig):
        for arg, orig_arg in zip(self.arguments, orig.arguments):
            arg.repairBinding(orig_arg)

    def isQ(self):
        return False

    def setIsVerb(self):
        self.isVerb = True

    def checkIfVerb(self):
        return self.isVerb

    def isConjV(self):
        return False

    def checkIfWh(self):
        is_lambda = self.__class__ == lambdaExp
        if is_lambda:
            has_e_var = self.getVar().type() == semType.e
            funct = self.getFunct()
            funct_is_lambda = funct.__class__ == lambdaExp
            if is_lambda and has_e_var and funct_is_lambda:
                return True
        else:
            return False

    #IDA: used only in genAllSplits
    # ## from pseudocode ##
    # def buildSubTree(self,pset):
    #     print "self is ",self.toString(True)
    #     newnode = self.copyNoVar()
    #     nout = []
    #     for i in range(len(self.arguments)):
    #         #print pset
    #         if pset[i][0].inout == self.inout:
    #             newnode.arguments[i]==pset[i][0]
    #             if pset[i][1] is not None:
    #                 nout.extend(pset[i][1])
    #         else:
    #             v = variable(None)
    #             a = pset[i][0]
    #             for k in range(len(pset[i][1])):
    #                 if pset[i][1][k]!=pset[i][1][k].linkedVar:
    #                     u = pset[i][1][k].linkedVar
    #                     v.addArg(pset[i][1][k])
    #                     al = lambdaExp()
    #                     al.setVar(u)
    #                     al.setFunct(a)
    #                     a = al
    #             v.arguments.reverse()
    #             a = a.copyNoVar()
    #             nout.append(a)
    #             v.setType(a.type())
    #             a.linkedVar = v
    #             newnode.setArg(i,v)
    #
    #     return (newnode,nout)

    #IDA: used only in genAllSplits
    # def buildAllSubTrees(self):
    #     nodename = self
    #     Q = [] #[])
    #     nodeout = []
    #     if len(nodename.arguments)==0 and self.__class__!=lambdaExp:
    #         print "args and that shit"
    #         print nodename.toString(True)
    #         if nodename.__class__ == variable:
    #             nodename.inout=nodename.binder.inout
    #             nodename.linkedVar = nodename
    #             Q.append((nodename,[nodename]))
    #             return Q
    #         newnode = nodename.copyNoVar()
    #         newnode.inout = True
    #         Q.append((newnode,nodeout))
    #         newnode = nodename.copyNoVar()
    #         newnode.inout = False
    #         Q.append((newnode,nodeout))
    #     # elif self.__class__==conjunction:
    #     #     newnode = nodename.copyNoVar()
    #     #     Q.append((newnode,[]))
    #     elif self.__class__==lambdaExp:
    #         return self.funct.buildAllSubTrees()
    #     else:
    #         A = []
    #         for i in range(len(nodename.arguments)):
    #             print "here innit"
    #             nodename.arguments[i].inout = None
    #             A.append(nodename.arguments[i].buildAllSubTrees())
    #         print "A is ",A
    #         for B in list(itertools.product(*A)):
    #             print "B is ",B
    #             if nodename.inout is None:
    #                 newnode = nodename.copyNoVar()
    #                 newnode.inout = True
    #                 (newnode,nodeout) = newnode.buildSubTree(B)
    #                 if len(nodeout)>2: continue
    #                 qseen = []
    #                 for l in list(itertools.permutations(nodeout)):
    #                     if (newnode,l) in qseen:
    #                         print "seen qperm "
    #                     qseen.append((newnode,l))
    #
    #                     Q.append((newnode,l))
    #             newnode = nodename.copyNoVar()
    #             newnode.inout = False
    #             (newnode,nodeout) = newnode.buildSubTree(B)
    #             if (newnode,nodeout) in Q:
    #                 print "duplicating in Q ",newnode.toString(True)
    #             Q.append((newnode,nodeout))
    #
    #     print "Q is ",Q
    #     qseen = []
    #     Q2 = []
    #     for q in Q:
    #         print "q is ",q
    #         if q[0].toString(True) in qseen:
    #             print "duplicated in q ",q, q[0].toString(True)
    #             for a in q[1]: print a.toString(True)
    #         else:
    #            Q2.append(q)
    #         qseen.append(q[0].toString(True))
    #     return Q2

    # IDA: not used
    # def genAllSplits(self):
    #     print "deffo here"
    #     pairsseen = []
    #     for node in self.allExtractableSubExps():
    #         for e in self.allExtractableSubExps():
    #             if not e in node.allExtractableSubExps():
    #                 e.inout = True
    #         print "node is ",node.toString(True)
    #         node.inout = False
    #         seena = []
    #         for (a,aout) in node.buildAllSubTrees():
    #
    #             v = variable(None)
    #             print "aout is ",aout
    #             print "before doing lambdas a is ",a.toString(True)
    #             for k in range(len(aout)):
    #                 v.arguments.append(aout[k])
    #                 u = aout[k].linkedVar
    #                 al = lambdaExp()
    #                 print "funct is ",aout[k].toString(True)
    #                 print "u is ",u
    #                 if u:
    #                     al.setVar(u)
    #                     al.setFunct(a)
    #                     a = al
    #                 else:
    #                     print "none u for ",aout[k].toString(True)
    #             v.arguments.reverse()
    #             v.setType(a.type())
    #             if a.toString(True) in seena:
    #                 print "duplicated a ",a.toString(True)
    #             else:
    #                 print "orig a ",a.toString(True)
    #             seena.append(a.toString(True))
    #             if node.__class__==lambdaExp:
    #                 origthing = node.getDeepFunct()
    #                 print "deep funct"
    #                 f = self.replace2(node.getDeepFunct(),v)
    #
    #             else:
    #                 f = self.replace2(node,v)
    #                 origthing = node
    #             fl = lambdaExp()
    #             fl.setFunct(f)
    #             fl.setVar(v)
    #             print "\n"
    #             print "a is ",a.toString(True)
    #             print "f is ",fl.toString(True)
    #             if (fl.toString(True),a.toString(True)) in pairsseen:
    #                 print "duplicated pair"
    #             print "pair is ",fl.toString(True)," ",a.toString(True)
    #             pairsseen.append((fl.toString(True),a.toString(True)))
    #             pair = ((fl.copy(),a.copy()))
    #             f = self.replace2(v,origthing)
    #             print "self back to ",self.toString(True)
    #
    #             self.resetLinkedVar()
    #             self.resetInOut()

            
    #def hasEvent(self):
        #self.event = eventMarker()
        #self.event.setBinder(self)
    #def checkIfHaveEvent(self):
        #return self.event!=None
    #def setEvent(self,ev):
        ##if not self.event: 
            ##error("trying to set event for "+self.toString(True))
            ##bang()
            ##print "self event is ",self.event
        ##else:
        #self.event=ev
        #ev.setBinder(self)


    #########################################
    # only lambdas should be allowed to apply
    # and compose.
    #########################################
    def apply(self,e):
        return None
    def compose(self,e):
        return None
            
    #########################################
    #def getEvent(self):
        #return self.event
    
    
    def setNounMod(self):
        self.nounMod = True

    def setIsNull(self):
        self.isNull=True

    def getIsNull(self):
        return self.isNull

    # def isNounMod(self):
    #     return self.nounMod
        # if self.posType in ["n","adj"]:
        #      #or \
        #     #self.name=="qn|other" or \
        #     #self.posType=="pro:indef":
        #     return True
        # return False

    def isEntity(self):
        return False

    def add_parent(self,e):
        if not e in self.parents:
            self.parents.append(e)

    def remove_parent(self,e):
        if e in self.parents:
            self.parents.remove(e)
            e.removeArg(self)
        elif e.__class__==eventSkolem and e.funct in self.parents:
            self.parents.remove(e.funct)
            e.funct.removeArg(self)
        else:
            print e.toString(True)," not in ",self.toString(True)," parents"
            print "parents are ",self.parents
            print "e is ",e

    def argsFilled(self):
        #print "this is ",self.name
        for a in self.arguments:
            #print a
            if a.isEmpty(): return False
        return True

    def setArg(self,position,argument):
        self.arguments.pop(position)
        self.arguments.insert(position,argument)
        if isinstance(argument,exp):
            argument.add_parent(self)
            self.argSet = True

    def getArg(self,position):
        if position>len(self.arguments)-1: error("only got "+str(len(self.arguments))+" arguments")
        else: return self.arguments[position]

    def numArgs(self):
        return len(self.arguments)
            
    def replace(self,e1,e2):
        # replaces all instances of e1 with e2r
        i=0
        for a in self.arguments:
            if a==e1: 
                #print "found match"
                self.setArg(i,e2)
                e2.add_parent(self)
            else: a.replace(e1,e2)
            i+=1

    # this version returns an expression
    def replace2(self,e1,e2):
        if self == e1:
            return e2
        i=0
        for a in self.arguments:
            self.arguments.pop(i)
            self.arguments.insert(i,a.replace2(e1,e2))
            i+=1
        return self
        
    ##########################################
    # this version uses python's inbuilt     #
    # lambda expression to deal with function#
    # definition. eep.                       #
    ##########################################
    def abstractOver(self,e):
        v = self.makeVariable(e)
        l = lambdaExp()
        l.setFunct(self)
        l.setVar(v)
        return l
    ###########################################
    # this function needs work!!!!            #
    # have ALL the code to do this elsewhere  #
    #                                         #
    # will need to:                           #
    #     - be able to recognise and abstract #
    #    over complex logical forms           #
    #    - abstract over one, or many of the  #
    #    same instance of an equivalent       #
    #    logical form.                        #
    ###########################################
    def makeVariable(self,e):
        if e in self.arguments:
            var = variable(e)
            self.arguments[self.arguments.index(e)] = var
            return var
        return None
        
    def bind(self,e):
        pass

    def copyNoVar(self):
        pass
        ## need to change for binders
        #return self.copy()

    def copy(self):
        print "copying ",self.toString(True)
        pass

    def makeShell(self):
        #args = []
        #for a in self.arguments:
            #args.append(a.copy())
        #e = exp(self.name,self.numArgs,self.argTypes,self.posType)
        #i=0
        #for a in args:
            #e.setArg(i,a)
            #i+=1
        #e.hasEvent()
        #e.setEvent(self.event)
        #if self.checkIfVerb(): e.setIsVerb()
        #return e
        pass

    def isEmpty(self):
        return False

    def getName(self):
        return self.name

    # var num will not work with different branches #
    def printOut(self,top,varNum):
        print self.toString(top)

    def toString(self,top):
        s=self.name
        if len(self.arguments)>0: s=s+"("
        for a in self.arguments:
            if isinstance(a,exp): s=s+a.toString(False)
            if self.arguments.index(a)<self.numArgs-1: s=s+","
        if len(self.arguments)>0: s=s+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        return s

    def toStringShell(self,top):
        s="placeholderP"
        if len(self.arguments)>0: s=s+"("
        for a in self.arguments:
            if isinstance(a,exp): s=s+a.toStringShell(False)
            if self.arguments.index(a)<self.numArgs-1: s=s+","
        if len(self.arguments)>0: s=s+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        return s

    def toStringUBL(self,top):
        s=self.name.replace(":","#")
        if len(self.arguments)>0: s="("+s+str(len(self.arguments))+":t "
        for a in self.arguments:
            if isinstance(a,exp): s=s+a.toStringUBL(False)
            if self.arguments.index(a)<self.numArgs-1: s=s+" "
        if len(self.arguments)>0: s=s+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        return s

    #IDA: not used
    # def missingArg(self,position):
    #     if position>=self.numArgs:
    #         return False
    #     if self.arguments[position].isEmpty(): return True
    #     return False

    #IDA: not used
    # def hasFilledArg(self,position):
    #     if position>=self.numArgs:
    #         return False
    #     if self.arguments[position].isEmpty(): return False
    #     return True

    def addArg(self,arg):
        self.arguments.append(arg)
        pass

    def setReturnType(self):
        pass

    def getReturnType(self):
        return self.returnType
        
    def type(self):
        print "shouldnt be asking for type here"
        error("shouldnt be asking for type here")

    def getPosType(self):
        if self.posType: return self.posType
        return None

    #IDA: used in other modules
    def top_node(self):
        if len(self.parents)==0: return self
        top = None
        for p in self.parents:
            if not p.top_node(): return None
            if top and top!=p.top_node():
                print top,"   ",p.top_node()
                return None
            top = p.top_node()
        return top

    def clearNames(self):
        for a in self.arguments:
            if a: a.clearNames()

    def equals(self,other):
        print "should never be getting here, equals defined on subexps"
        print "this is ",self.toString(True)
        error("should never be getting here, equals defined on subexps")
        
    def equalsPlaceholder(self,other):
        print "should never be getting here, equals defined on subexps"
        print "this is ",self.toString(True)
        error("should never be getting here, equals defined on subexps")

    #IDA: only used in makePairs2()
    # def resetEqualOther(self):
    #     for e in self.allSubExps():
    #         if e.__class__ == variable:
    #             e.equalother = None

    #IDA: only used in makePairs2() and genAllSplits()
    # def resetLinkedVar(self):
    #     for e in self.allSubExps():
    #         e.linkedVar = None
    #     vset = []
    #     e.getAllVars(vset)
    #     for v in vset:
    #         v.linkedVar = None

    #IDA: only used in makePairs2() and genAllSplits()
    # def resetInOut(self):
    #     for e in self.allSubExps():
    #         e.inout = None
    #     vset = []
    #     e.getAllVars(vset)
    #     for v in vset:
    #         v.inout = None

    def clearParents(self):
        self.parents = []
        for a in self.arguments:
            a.clearParents()

    def clearParents2(self):
        self.parents = []

    def removeArg(self,arg):
        for i in range(len(self.arguments)):
            a = self.arguments[i]
            if a==arg: 
                self.arguments.pop(i)
                return

    def recalcParents(self,top):
        if top:
            self.clearParents()
        for a in self.arguments:
            a.add_parent(self)
            a.recalcParents(False)
    
    def allSubExps(self):
        subExps = []
        subExps.append(self)
        for d in self.arguments:
            subExps.extend(d.allSubExps())
        return subExps

    def allExtractableSubExps(self):    
        subExps = []
        subExps.append(self)
        for d in self.arguments:
            subExps.extend(d.allExtractableSubExps())
        return subExps

    #IDA:seems not to be used
    # def makeTree(self,inNodes,outNodes):
    #     pass

    #IDA:seems not to be used
    # def allTrees(self):
    #     selfTrees = []
    #     selfTrees.append(self)
    #     argTrees = []
    #     for a in self.arguments:
    #         argTrees.append(a.allTrees())
    #
    #     combs = getCombs(argTrees)
    #     return selfTrees

    def allArgs(self):
        return self.arguments

    def getAllVars(self,vars):
        for a in self.arguments:
            a.getAllVars(vars)

    def varsAbove(self,other,vars):
        if self==other: return
        for a in self.arguments:
            a.varsAbove(other,vars)

    def unboundVars(self):
        boundVars = []
        vars = []
        subExps = self.allSubExps()
        for e in subExps:
            if e.__class__ == variable and e.binder:
                if e.binder in subExps:
                    boundVars.append(e)
            # try:
            #     boundVars.append(e.var)
            # except AttributeError:
            #     pass
            # if e.__class__ in [lambdaExp,quant,eventSkolem]:
            #     boundVars.append(e.var)
        self.getAllVars(vars)
        unboundvars = []
        for v in vars:
            if not v in boundVars and v!=self: unboundvars.append(v)
        # higher nested things at front
        #unboundvars.reverse()
        return unboundvars
        
    def partitionVars(self,other):
        allVars = []
        self.getAllVars(allVars)
        aboveVars = []
        self.varsAbove(other,aboveVars)
        belowVars = []
        other.getAllVars(belowVars)
        bothVars = []
        for v in allVars:
            if v in belowVars:
                bothVars.append(v)
        return (belowVars,aboveVars,bothVars)
        
        
    # really want a function that takes an
    # expression and two lists of nodes. One
    # to remain with the expression and one 
    # to be pulled out. Will return a new 
    # (with no root level lambda terms) and 
    # a variable (with root level lambda terms).


    # return a pair copy for each way to pull the thing
    # out. can be > 1 because of composition.
    # each pair needs to say how many lambda terms go 
    # with composition.
    # just have a different definition in lambdaExp???
    def pullout(self,e,vars,numNewLam):
        vargset = []
        for v in vars:
            vset = []
            for a in v.arguments:
                vset.append(a)
            vargset.append(vset)
            
        
        # first of all, make function application
        origsem = self.copy()
        orige = e.copy()
        pairs = []
        (belowvars,abovevars,bothvars) = self.partitionVars(e)
        ec = e.copyNoVar()
        
        if self.__class__==lambdaExp and len(vars)>0:
            compdone = False
            frontvar = self.var
        else:
            compdone = True
        varindex = len(vars)-1
        compp = self
        compvars = []
        numByComp = 0
        while not compdone:
            current_v = vars[varindex]
            if current_v == self.var and current_v not in abovevars and not current_v.isEvent:
                compvars.append(vars[varindex])
                numByComp += 1
                p = compp.compositionSplit(vars,compvars,ec,e)
                ptuple = (p[0],p[1],numNewLam,numByComp)
                pairs.append(ptuple)
                if compp.funct.__class__==lambdaExp and\
                 len(vars)>varindex+1:
                    varindex-=1
                    compp = compp.funct
                    frontvar=self.funct.var
                else: compdone = True
            else: compdone = True

        # all sorts of composition shit in here
        ec = e.copyNoVar()
        newvariable = variable(ec)
        self.replace2(e,newvariable)
        p = self.copyNoVar()
        

        for v in vars:
            nv = variable(v)
            nv.arguments = v.arguments
            ec.replace2(v,nv)
            # this line is definitely not always right
            #vargset.append(v.arguments)
            v.arguments = []
            newvariable.addAtFrontArg(v)                
            l = lambdaExp()
            l.setFunct(ec)
            l.setVar(nv)
            ec = l
        
        newvariable.setType(ec.type())
        
        l = lambdaExp()
        l.setFunct(p)
        l.setVar(newvariable)
        pair = (l.copy(),ec.copy(),numNewLam,0)
        pairs.append(pair)
        
        self.replace2(newvariable,e)
    
        i=0
        for v in vars:
            v.arguments = vargset[i]
            i+=1

        l1 =  pair[0].copy()
        e1 = pair[1].copy()

        try:
            sem = l1.apply(e1)
        except AttributeError:
            sem = l1.apply(e1)

        e.repairBinding(orige)
        self.repairBinding(origsem)
        # if sem == None:
        #     sem = l1.apply(e1)
        if not sem.equals(self):
            print "sems dont match : "+sem.toString(True)+"  "+self.toString(True)
        # if not self.equals(origsem):
        #     print "\nnot back to orig"
        #     print self.toString(True)
        #     print origsem.toString(True)
        #     print ""
        return pairs

    def arity(self):
        return 0

    def hasVarOrder(self,varorder):
        varnum = 0
        for a in self.arguments:
            if a.__class__ == variable:
                if a.name!=varorder[varnum]:
                    return False
                varnum+=1
        if varnum!=len(varorder):
            return False
        return True        

    def varOrder(self,L):
        """Omri added 25/7"""
        varnum = 0
        for a in self.arguments:
            if a.__class__ == variable:
                L[varnum] = a.name
                varnum+=1
            
    def getNullPair(self):
        ## this should ALWAYS be by composition
        # parent, child
        child = self.copy()
        parent = lambdaExp()

        var = variable(self)
        parent.setVar(var)
        parent.setFunct(var)
        # all the child cats will have fixed dir and 
        # there are no new lambdas in the arg
        
        # maybe forget the actual direction just the content
        # fixeddircats will actually have the variables
        fixeddircats = []
        f = self
        done = not (f.__class__==lambdaExp)
        while not done:
            if not f.__class__==lambdaExp:
                print "not a lambda expression, is  ",f.toString(True)  
                error("not a lambda expression")
            fixeddircats.append(f.var)
            if not f.funct.__class__==lambdaExp: done = True
            else: f = f.funct
            
        return (parent,child,0,0,None)
        
        
    def split_subexp(self,e):
        if self.arity() > 3: return []
        allpairs = []
        self.recalcParents(True)
        origsem = self.copy()
        child = e
        sem = self
        
        evars = e.unboundVars()
        # control the arity of the child
        # this may well be problematic        
        if len(evars)>4: return (None,None)
        ordernum=0
        
        (orders,numNewLam,fixeddircats) = self.getOrders(evars)
        for order in orders:
            ordernum+=1
            splits = self.pullout(e,order,numNewLam)
            for parentSem, childSem, numNewLam, numByComp in splits:
                allpairs.append((parentSem, childSem, numNewLam, numByComp, fixeddircats))
                # this should be limited, can only do if none by comp
                # parentSem = splittuple[0]
                # childSem = splittuple[1]
                if self.allowTypeRaise:
                    if numByComp==0:
                        if childSem.canTypeRaise():
                            typeRaisedChild = childSem.typeRaise(parentSem)
                            print "Type raised child is : "+typeRaisedChild.toString(True)
                            print "Parent Sem is : "+parentSem.toString(True)
                            # don't know what to do with the newLam integer
                            trfc =  ["typeraised"]
                            trfc.extend(fixeddircats)
                            allpairs.append((typeRaisedChild, parentSem.copy(), numNewLam ,0,trfc))
            if len(order)!=len(evars): print "unmatching varlist lengths"
        return allpairs

    def canTypeRaise(self):
        #if self.type().equals(semType.e): return True
        return True

    def typeRaise(self,parent):
        v = variable(parent)
        v.addArg(self.copy())
        l = lambdaExp()
        # it's an opaque way of setting it up,
        # but child is now an argument to which whatever
        # replaces the variable will be applied
        l.setVar(v)
        l.setFunct(v)
        return l
            
    def getOrders(self,undervars):
        # if the order is defined by the lambda terms of this
        # thing then go with that order but otherwise we need to 
        # get iterations.
        uv2 = []
        evm = None
        for v in undervars: 
            if v.__class__ == eventMarker:
                if evm: print "already got event marker"
                evm = v
            else: uv2.append(v)
        
        fixedorder = []
        
        for lvar in self.getLvars():
            if lvar in undervars:
                fixedorder.append(lvar)
                del uv2[uv2.index(lvar)]
        
        orderings = []
        if len(uv2)==0:
            ordering = []
            for v in fixedorder: ordering.append(v)
            if evm:    ordering.append(evm)
            ordering.reverse()
            orderings.append(ordering)
        else:
            for perm in permutations(uv2):
                ordering = []
                for v in fixedorder: ordering.append(v)
                ordering.extend(perm)
                if evm:
                    ordering.append(evm)
                ordering.reverse()
                orderings.append(ordering)
        return (orderings,len(uv2) +((evm or 0) and 1) , fixedorder)
        
        
    def getLvars(self): return []

    #IDA:seems not to be used
    def getheadlambdas(self):
        return []

    #IDA:seems not to be used
    def markCanBePulled(self):
        for e in self.allSubExps():
            pass
    #IDA: not used
    # def getCanBePulled(self):
    #     pass

    #IDA: used only in makePairs2()
    # def setInOut(self,inout):
    #     self.inout = inout
    #
    # def setInOuts(self):
    #     for e in self.allSubExps():
    #         if e==self: continue
    #         inout = random.random()>0.5
    #         e.setInOut(inout)

    #IDA: only used in makePairs2()
    # this is going to pull out all nested things too.
    # make 
    # def makeInOut(self):
    #     # make logical form and variable
    #     selfnew = self.copyNoVar()
    #     outargs = set()
    #     vset = set()
    #     i = 0
    #     for a in self.arguments:
    #         (anew,aout,avset) = a.makeInOut()
    #         print "dealing with arg ",i," which gives ",anew.toString(True)," in ",self.toString(True)
    #         print "dealing with arg ",str(id(a))," in ",self.toString(True)
    #
    #         print "a.inout = ",a.inout," this inout = ",self.inout
    #         if a.inout==self.inout or a.inout is None:
    #             print "selfnewnow is ",selfnew.toString(True)
    #             print "len args is ",len(selfnew.arguments)
    #             print "i is ",i
    #             print "anew is ",anew.toString(True)
    #             selfnew.setArg(i,anew)
    #             print "selfnewnow is ",selfnew.toString(True)
    #             #outargs.extend(aout)
    #             #vset.extend(avset)
    #             outargs = outargs.union(aout)
    #             vset = vset.union(avset)
    #         else:
    #             if anew.linkedVar is not None:
    #                 print "got linkedVar for ",anew.toString(True),str(id(anew)),"  in ",self.toString(True)
    #                 v = anew.linkedVar
    #                 selfnew.setArg(i,v)
    #             else:
    #
    #                 v = variable(None)
    #                 print "making var for ",anew.toString(False)#," but have variables ",
    #                 print "setting new arg in ",selfnew.toString(True)
    #
    #                 selfnew.setArg(i,v)
    #                 print "now is ",selfnew.toString(True)
    #                 # where do the variables go?
    #                 lambdaord = []
    #                 for outarg in aout:
    #                     v.addArg(outarg)
    #                     if outarg.linkedVar is None:
    #                         print "\n\noutarg linkedvar is none"
    #                     else:
    #                         print outarg.linkedVar.toString(True),
    #                         lambdaord.append(outarg.linkedVar)
    #                 for lambdavar in reversed(lambdaord):
    #                     l = lambdaExp()
    #                     l.setVar(lambdavar)
    #                     l.setFunct(anew)
    #                     anew = l
    #
    #                 v.setType(anew.type())
    #                 print "setting linkedVar for ",anew.toString(True)
    #                 anew.linkedVar = v
    #                 vset.add(v)
    #
    #             print " anew now is ",anew.toString(True)
    #             # for outv in avset:
    #             print "\n\n"
    #             outargs.add(anew)
    #         i+=1
    #     return (selfnew,outargs,vset)

    #IDA: only used in makePairs2()
    # def makeSplit(self,undere):
    #     eorig = self.copy()
    #     print "\n\nundere is ",undere.toString(True)
    #     if undere.__class__ == lambdaExp: return None
    #     if self.__class__ == lambdaExp and undere==self.funct: return None
    #
    #     selfnew = self.copy()
    #     (anew,outs,vset) = undere.makeInOut()
    #
    #     v = variable(anew)
    #     lambdaord = []
    #     for a in outs:
    #         print "aout is ",a.toString(True),a
    #         v.addArg(a)
    #         lambdaord.append(a.linkedVar)
    #     print "lambdaord is ",len(lambdaord)," long"
    #     for lambdavar in reversed(lambdaord):
    #         l = lambdaExp()
    #         l.setVar(lambdavar)
    #         l.setFunct(anew)
    #         anew = l
    #         # REALLY NEED TO MATCH VARIABLE ORDER TO ARG
    #         # ORDER AND LAMBDA ORDER
    #     print "v is ",id(v)
    #     v.setType(anew.type())
    #     print "self before replace is ",self.toString(True)
    #     print "undere is ",undere.toString(True)
    #     self.replace2(undere,v)
    #     print "self is ",self.toString(True)
    #     enew = self.copyNoVar()
    #
    #     l = lambdaExp()
    #     l.setVar(v)
    #     l.setFunct(enew)
    #     print "l is ",l.toString(True)
    #     enew = l.copy()
    #
    #     print "pairMS is ",enew.toString(True),anew.toString(True)
    #     pair = (enew.copy(),anew.copy())
    #     eback = enew.apply(anew)
    #     self.replace2(v,undere)
    #     print "self back to ",self.toString(True)
    #     if eback:
    #         print "enew back to ",eback.toString(True)
    #         eback.resetEqualOther()
    #         eorig.resetEqualOther()
    #         eback.resetLinkedVar()
    #         eorig.resetLinkedVar()
    #         eback.resetInOut()
    #         eorig.resetInOut()
    #
    #         if not eback.equals(eorig):
    #             print "got enew but not back to orig ",eback.toString(True)
    #         else:
    #             print "equals orig"
    #     else:
    #         print "enew back to None"
    #         self.replace2(v,undere)
    #         print "eback to ",self.toString(True)
    #         if not eorig.equals(self):
    #             print "not back to orig"
    #         print "******* DONE *********"
    #     print "returning ",pair
    #     return pair
    #
    #     # v = variable(anew)
    #     # for a in outs:
    #     #     print "aout is ",a.toString(True),a
    #     #     v.addArg(a)
    #     #
    #     # # REALLY NEED TO MATCH VARIABLE ORDER TO ARG
    #     # # ORDER AND LAMBDA ORDER
    #     #
    #     # print "a1 is ",anew.toString(True)
    #     # print "e is ",self.toString(True)
    #     #
    #     # # do not want to do this
    #     # self.replace2(undere,v)
    #     # for av in vset:
    #     #     l = lambdaExp()
    #     #     l.setVar(av)
    #     #     l.setFunct(anew)
    #     #     anew = l
    #     #
    #     #
    #     #
    #     # print "Anew is ",anew.toString(True)
    #     # #    print "Vnew is ",v.toString(True)
    #     #
    #     # enew = self.copyNoVar()
    #     # l = lambdaExp()
    #     # l.setVar(v)
    #     # l.setFunct(enew)
    #     # enew = l.copy()
    #     #
    #     # print "here ENew is ",enew.toString(False)
    #     # self.replace2(v,undere)
    #     # print "self back to ",self.toString(True)
    #     # return (enew,anew)

    #IDA: not used
#     def makePairs2(self,depth=1):
#         if depth>6: return
#         depth = depth+1
#         pairs = []
#         print "splitting ",self.toString(True)
#         seentypes = []
#         conjunctions = []
#         numsplits = 0
#         print "self in makepairs 2 is ",self.toString(True)
#         subExps = self.allExtractableSubExps()
#         for e in subExps:
#             if e == self: continue
#             nu = 0
#             print "e is ",e.toString(True)
#             for e2 in e.allExtractableSubExps():
#                 if e2 == e: continue
#                 if e2.__class__==variable: continue
#                 # not sure that we have a decent thing going
#                 # on with return type but that can be fixed
#                 nu += 1
#             numsplits += pow(2,nu)
#             for i in range(pow(2,nu)):
#                 e.resetBinders()
#                 for unune in e.allSubExps():
#                     unune.linkedVar = None
#                     print "setting to false for ",unune.toString(True)
#                     unune.setInOut(False)
#
#                 bi = list(bin(i)[2:])
#                 # need to pack bi with zeroes
#                 for j in range(len(bi),nu): bi.insert(0,0)
#                 print "bi is ",bin(numsplits)[2:]
#                 j = 0
#                 for e2 in e.allExtractableSubExps():
#                     if e2 == e: continue
#                     if e2.__class__==variable: continue
#
#                     print "e2 is ",e2.toString(True)
#                     if  bi[j]==0:  e2.setInOut(False)
#                     else: e2.setInOut(True)
#                     j+=1
#                 vset = []
#                 e.getAllVars(vset)
#                 for v in vset: v.setVarInOut()
#
#                 pair = self.makeSplit(e)
#                 if pair and pair[0] and pair[1]:
# #                    pair[0].makePairs2()
# #                    pair[1].makePairs2()
# #                print "made pair, self is ",self.toString(True)
#                     pairs.append((pair[0].copy(),pair[1].copy(),0,0,0))
# #                    pairs[-1][0].makePairs2(depth)
# #                    pairs[-1][1].makePairs2(depth)
#                 if pair is not None:
#                     print "i is ",i," bi is ",bi,"pair is ",pair[0].toString(True),pair[1].toString(True)
#                     print "pair is ",pair[0].toString(True),pair[1].toString(True)
#
#             print "numsplits i= ",numsplits
#         return pairs

    # to do in make pairs:
    # 1. want to be able to pull a variable out in one 
    # place only (or in multiple places simultaneously).
    # 2. want to get all subtrees in there. this will 
    # cause a ridiculous blowup in complexity...
    # 
    # CONSTRAINTS: is across board constraint ok with
    # prepositions????
    # how to do A-over-A constraint???
            
    def makePairs(self):
        #self.makePairs2()
        if self.nullSem(): return []
        repPairs = []
        subExps = self.allExtractableSubExps()
        # ooh, remember this is hard
        # do split, copy then reapply
        
        conjunctions = []
        for e in subExps:

            # this is how we should add null if we're going to
            allowNull = True
            if e==self: 
                if allowNull:
                    nullpair = self.getNullPair()
                    repPairs.append(nullpair)
                continue
            if e.__class__==variable:# and e.arguments==[]:
                continue
                #return (None,None)
            if e.__class__==eventMarker: continue
            ##print "subExp : ",e.toString(True)
            # if e.__class__==conjunction:
            #     #print e.toString(True)," is a conjunction"
            #     conjunctions.append(e)
            #else:
            repPairs.extend(self.split_subexp(e))
            
            #repPairs.extend
        #IDA: conjunctions should be treated differently because of across-the-board constraint?
        for conj in conjunctions:
            pass
            # for each conjunction order, in vs out
            #conjsplits = conj.getconjsplits()
            #for (inconj,outconj) in conjsplits:
                #print "conjsplit ",(inconj,outconj)
                #if len(outconj.arguments)<2 or len(inconj.arguments)<1: 
                    #continue
                #self.splitconj(conj,inconj,outconj)
                #print "conj is ",conj
                
                
            #repPairs.extend(c.splitconj())
        return repPairs
    #def setFunct(self,exp):
        #self.funct = exp
        #exp.add_parent(self)
    #def setVar(self,var):
        #self.var = var

    def nullSem(self):
        return False

    def abstractOver(self,e,v):
        i=0
        for a in self.arguments:
            if a==e:
                self.setArg(i,v)
        for a in self.arguments:
            a.abstractOver(e,v)

    #IDA: I give up on making main() work, for now
    # @staticmethod
    # def main():
    #     # What are you doing in that PLACEHOLDER
    #     r1 = makeExpWithArgs("lambda $0_{e}.lambda $1_{ev}.and(aux|be&PRES(part|do-PROG(pro|you,$0,$1),$1),prep|in(det|that($2,n|placeholderP($2)),$1))",{})
    #     # I don't want you to trip on your shoelace
    #     r2 = makeExpWithArgs("lambda $0_{ev}.not(and(aux|do(and(v|want(pro|I,pro|you,$0),v|trip(pro|you,$0)),$0),prep|on(pro:poss:det|your($1,n|shoelace($1)),$0)),$0)",{});
    #     # Did you find the little red bicycle?
    #     r3 = makeExpWithArgs("lambda $0_{ev}.Q(aux|do&PAST(v|find(pro|you,det|the($1,and(adj|little($1),and(adj|red($1),n|bicycle($1)))),$0),$0))",{})
    #     # She is going to have a bottle
    #     r4 = makeExpWithArgs("lambda $0_{ev}.aux|be&3S(and(part|go-PROG(pro|she,$0),v|have(pro|she,det|a($1,n|bottle($1)),$0)),$0)",{});
    #     # same as r2?
    #     r4 = makeExpWithArgs("lambda $0_{ev}.not(aux|do(v|want(pro|I,lambda $1_{ev}.and(v|trip(pro|you,$1),prep|on(det:poss|your($2,n|shoelace($2)),$1)),$0),$0))",{})
    #
    #
    #     print "made reps\n\n"
    #     e1 = r1[0]
    #     e2 = r2[0]
    #     print "r1 = r2? Should be false: "
    #     print e1.equals(e2)
    #     print "r1 = r2, accounting for placeholders? Should be false: "
    #     print e1.equalsPlaceholder(e2)
    #
    #     print "\n\nPrint-out of expression 4:"
    #     e = r4[0]
    #     e.printOut(True,0)
    #     print "\n\nCopying expression 4:"
    #     eorig = e.copy()
    #
    #     # Test all methods of splitting an expression
    #     print "\n\nMaking splits of expression 4, makePairs():"
    #     e4 = r4[0]
    #     b = e4.makePairs()
    #     print "\n\nmakePairs() done."
    #     print "\n\nMaking splits of expression 4, genAllSplits():"
    #     e4.genAllSplits()
    #     print "\n\ngenAllSplits() done"
    #     # return
    #     print "\n\nMaking splits of expression 4, makePairs2():"
    #     a = e4.makePairs2()
    #     print "makePairs2() done\n\n\n"
    #
    #     #
    #     for p in a:
    #         print "pair2",p[0].toString(True),p[1].toString(True)
    #     print len(a), " from makepairs2"
    #     return
    #
    #     print "\nExp Splits are:"
    #     for split in e.makePairs():
    #         print split[0].toString(True)," ",split[1].toString(True)
    #     print "\n\n\n\n"
    #     i = 0
    #     for undere in e.allSubExps():
    #         if undere.__class__==variable: continue
    #         print "e now is ",e.toString(True)
    #         e.resetBinders()
    #         for unune in e.allSubExps():
    #             unune.linkedVar = None
    #             print "setting to false for ",unune.toString(True)
    #             unune.setInOut(False)
    #         print "\n\nundere is ",undere.toString(True)
    #         if undere.__class__ == lambdaExp: continue
    #         if e.__class__ == lambdaExp and undere==e.funct: continue
    #         undere.setInOut(True)
    #
    #         undere.setInOuts()
    #         vset = []
    #         e.getAllVars(vset)
    #         for v in vset: v.setVarInOut()
    #         selfnew = e.copy()
    #         print "making inout"
    #         (anew,outs,vset) = undere.makeInOut()
    #         print "made inout"
    #         print "ANEW WITH LAMBDA IS ",anew.toString(True)
    #         v = variable(anew)
    #         lambdaord = []
    #         for a in outs:
    #             print "aout is ",a.toString(True),a
    #             v.addArg(a)
    #             lambdaord.append(a.linkedVar)
    #         for lambdavar in reversed(lambdaord):
    #             l = lambdaExp()
    #             l.setVar(lambdavar)
    #             l.setFunct(anew)
    #             anew = l
    #         # REALLY NEED TO MATCH VARIABLE ORDER TO ARG
    #         # ORDER AND LAMBDA ORDER
    #         v.setType(anew.type())
    #
    #         print "a1 is ",anew.toString(True)
    #         print "e is ",e.toString(True)
    #
    #         e.replace2(undere,v)
    #
    #         print "Anew is ",anew.toString(True)
    #         print "e1 is ",e.toString(True)
    #
    #         enew = e.copyNoVar()
    #         print "enew1 is ",enew.toString(True)
    #         l = lambdaExp()
    #         l.setVar(v)
    #         l.setFunct(enew)
    #
    #         enew = l.copy()
    #
    #         print "here2 ENew is ",enew.toString(False)
    #         print "pair is ",enew.toString(True),anew.toString(True)
    #
    #         eback = enew.apply(anew)
    #
    #         if eback:
    #             print "enew back to ",eback.toString(True)
    #             eback.resetEqualOther()
    #             eorig.resetEqualOther()
    #             if not eback.equals(eorig):
    #                 print "got enew but not back to orig ",eback.toString(True)
    #             else:
    #                 print "equals orig"
    #         else:
    #             print "enew back to None"
    #         e.replace2(v,undere)
    #         print "eback to ",e.toString(True)
    #         if not eorig.equals(e):
    #             print "not back to orig"
    #         print "******* DONE *********"


class emptyExp(exp):
    def __init__(self):
        self.name = "?"
        self.numArgs = 0
        self.argTypes = None
        self.arguments = []
        self.parents = []
        self.argSet = False
        #self.event=None
        self.isVerb=False
        self.returnType = None
        self.isNull = False
        self.inout = None
        self.doubleQuant = False

    def makeShell(self, expDict):
        if self in expDict:
            e = expDict[self]
        else:
            e = emptyExp
        expDict[self] = e
        return e

    def copy(self):
        return emptyExp()

    def copyNoVar(self):
        return emptyExp()

    def isEmpty(self):
        print "this is empty"
        return True

    def allSubExps(self):
        return []

    def allExtractableSubExps(self):
        return []

    def toString(self,top):
        if self.name=="?":
            self.name="?"+str(exp.emptyNum)
            exp.emptyNum+=1
        s=self.name
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            # self.clearNames()
        return s

    def toStringUBL(self,top):
        if self.name=="?":
            self.name="?"+str(exp.emptyNum)
            exp.emptyNum+=1
        s=self.name
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            # self.clearNames()
        return s

    def clearNames(self):
        self.name="?"

    def equalsPlaceholder(self,other):
        if other.__class__ != emptyExp: return False
        return True

    def equals(self,other):
        if other.__class__ != emptyExp: return False
        return True

            
class variable(exp):
    def __init__(self,e):
        self.linkedVar = None
        self.name = None
        self.arguments = []
        self.parents = []
        #self.event=None
        self.isVerb=False
        self.binder = None
        self.equalother = None
        self.varcopy = None
        self.posType=None
        self.inout=None
        self.doubleQuant = False
        self.nounMod = False
        self.bindVar = None
        self.varIsConst = None
        if e:
            #if e is a quant type of predicate
            try:
                self.bindVar = e.bindVar
                if self.bindVar:
                    # self.varIsConst = True
                    self.varIsConst = e.varIsConst
            except AttributeError:
                pass
            self.t = e.type()
            self.numArgs = e.numArgs
            self.argTypes = e.argTypes
            #self.arguments = []
            #for a in e.arguments:
                #print "adding arg ",a
                #self.addAtFrontArg(a)
            #self.arguments = e.arguments
            self.returnType = e.getReturnType()
            # if e is a predicate
            # self.nounMod = e.isNounMod()
            # if e is a variable
            try:
                self.isEvent = e.isEvent
            except AttributeError:
                self.isEvent = False
        else:
            self.numArgs = 0
            self.argTypes = []
            self.arguments = []
            # assume that we only introduce entity
            # vars from the corpus
            #self.returnType = "e"
            self.returnType = semType.eType()
            self.t = semType.eType()
            self.isEvent = False
        self.isNull = False

    def setArgHelper(self, position, argument):
        self.arguments.pop(position)
        self.arguments.insert(position,argument)
        if isinstance(argument,exp):
            argument.add_parent(self)
            self.argSet = True

    def setArg(self,position,argument):
        if not self.bindVar:
            self.setArgHelper(position, argument)
        else:
            if position == 0:
                if argument.__class__ == variable and not argument.isEvent:
                    if self.varIsConst == None:
                        argument.setBinder(self)
                        self.varIsConst = False
                        self.returnType = semType.eType()
                        # self.nounMod = True
                else:
                    if self.varIsConst == None:
                        self.varIsConst = True
                self.setArgHelper(position, argument)
            if position >= 1:
                if self.varIsConst:
                    for a in argument.allArgs():
                        if a.equals(self.arguments[0]):
                            argument.replace2(a, self.arguments[0])
                self.setArgHelper(position, argument)
            # if position>1:
            #     if argument.__class__ == eventMarker or (argument.__class__ == variable and argument.isEvent):
            #         self.setArgHelper(position, argument)
            #     else:
            #         error("only eventMarker acceptable as second arg for quant")

    def setVarInOut(self):
        self.inout = self.binder.inout
        if self.inout == None:
            self.inout = True
        print "self.binder is ",self.binder.toString(True)
        print "set inout for ",str(id(self))," to ",self.inout

    def type(self):
        return self.t

    def setBinder(self,e):
        self.binder = e

    def semprior(self):
        p = 0.0
        for a in self.arguments:
            p += a.semprior()
        return p

    def vartopprior(self):
        return -2.0
        #return self.semprior()
        #return -3 * self.type().toString().count(",") - 1

    def makeShell(self, expDict):
        if self.varcopy:
            v = self.varcopy
        elif self in expDict:
            v = expDict[self]
        else:
            v = variable(self)
            v.name = self.name
            expDict[self] = v
        # if self.varcopy is None:
            # return None
            # v = variable(self)
            # self.varcopy = v
        # else:
        #     v = self.varcopy
        args = []
        for a in self.arguments:
            args.append(a.makeShell(expDict))
        v.arguments = args
        return v

    def isEmpty(self):
        return False

    # def isConjN(self):
    #     return False

    def copy(self):
        if self.varcopy is None:
            return None
        # variable with no arguments
        v = self.varcopy
        v.linkedVar = self.linkedVar
        v.arguments = []
        v.varIsConst = self.varIsConst
        if self.arguments:
            v.arguments = [None for a in self.arguments]
            if not self.bindVar or (self.bindVar and self.varIsConst):
                arg0Bound = False
            else:
                arg0Bound = self.arguments[0].binder == self
            # variable in place of normal predicate
            # if not self.bindVar or (self.bindVar and len(self.arguments) == 1):
            if not self.bindVar or not arg0Bound:
                args = []
                for a in self.arguments:
                    args.append(a.copy())
                for i, a in enumerate(args):
                    v.setArg(i,a)
            else:
                # variable in place of quant with bound variable
                if not self.varIsConst:
                    newvar = variable(None)
                    self.arguments[0].setVarCopy(newvar)
                # variable in place of quant with constant
                else:
                    newvar = self.arguments[0].copy()
                args = [newvar]
                args.extend([a.copy() for a in self.arguments[1:]])
                for i, a in enumerate(args):
                    v.setArg(i,a)
        return v

    def copyNoVar(self):
        return self

    # def copyNoVar(self):
    #     # variable with no arguments
    #     if not self.arguments:
    #         return self
    #     else:
    #         v = self.varcopy
    #         v.linkedVar = self.linkedVar
    #         v.arguments = [None for a in self.arguments]
    #         # variable mimicking predicate
    #         if not self.bindVar:
    #             args = []
    #             for a in self.arguments:
    #                 args.append(a.copyNoVar())
    #         # variable mimicking quant
    #         else:
    #             # with first arg being a constant
    #             if self.varIsConst:
    #                 args = [a.copyNoVar() for a in self.arguments]
    #             # with first arg being a variable
    #             else:
    #                 args = [self.arguments[0]]
    #                 args.extend([a.copyNoVar() for a in self.arguments[1:]])
    #         for i, a in enumerate(args):
    #             v.setArg(i,a)
    #     return v

    def allSubExps(self):
        subexps = [self]
        if len(self.arguments)>0:
            # subexps.append(self)
            for a in self.arguments:
                subexps.extend(a.allSubExps())
        return subexps

    def allExtractableSubExps(self):
        subexps = []
        if len(self.arguments)>0:
            for a in self.arguments:
                subexps.extend(a.allExtractableSubExps())
        return subexps

    def getAllVars(self,vars):
        if not self in vars:
            vars.append(self)
        for a in self.arguments:
            a.getAllVars(vars)

    def varsAbove(self,other,vars):
        if self==other: return
        if not self in vars:
            vars.append(self)
        for a in self.arguments:
            a.varsAbove(other,vars)

    def addAtFrontArg(self,arg):
        self.arguments.insert(0,arg)

    def toString(self,top):
        s=""
        if not self.name:
            self.name="UNBOUND"#+str(id(self)) #exp.varNum)
        s=self.name #+str(id(self))#+"_{"+self.type().toString()+"}"#"_"+str(id(self))+"_{"+self.type().toString()+"}"
        if self.arguments!=[]: s = s+"("
        for a in self.arguments:
            if a is None:
                print "none arg"
                s=s+"NONE"+str(a)
            else:
                s=s+a.toString(False)
            if self.arguments.index(a)<(len(self.arguments)-1):
                s=s+","
        if self.arguments!=[]: s = s+")"

        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            # self.clearNames()
        return s

    def toStringShell(self,top):
        s=""
        if not self.name:
            self.name="UNBOUND"#+str(id(self)) #exp.varNum)
        s=self.name#+"_{"+self.type().toString()+"}"#"_"+str(id(self))+"_{"+self.type().toString()+"}"
        if self.arguments!=[]: s = s+"("
        for a in self.arguments:
            if a is None:
                print "none arg"
                s=s+"NONE"+str(a)
            else:
                s=s+a.toStringShell(False)
            if self.arguments.index(a)<(len(self.arguments)-1):
                s=s+","
        if self.arguments!=[]: s = s+")"

        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            # self.clearNames()
        return s

    def toStringUBL(self,top):
        s=""
        if not self.name:
            self.name="UNBOUND"#+str(id(self)) #exp.varNum)
        s=self.name#+"_{"+self.type().toString()+"}"#"_"+str(id(self))+"_{"+self.type().toString()+"}"
        if self.arguments!=[]: s = "("+s
        for a in self.arguments:
            if a is None:
                print "none arg"
                s=s+"NONE"+str(a)
            else:
                s=s+a.toStringUBL(False)
            if self.arguments.index(a)<(len(self.arguments)-1):
                s=s+" "
        if self.arguments!=[]: s = s+")"

        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s

    def clearNames(self):
        self.name=None
        for a in self.arguments:
            a.clearNames()

    def apply(self,other):
        print "cannot apply variable ",self
        error()
    # checking equality here is tricky because the
    # order of the lambda expressions is important

    # call this whenever introducing a variable
    def setEqualTo(self,other):
        self.equalother = other

    def setVarCopy(self,other):
        self.varcopy = other

    def equalType(self,other):
        if other.__class__ != variable: return False
        if not other.type().equals(self.type()): return False
        return True

    def setType(self,t):
        self.t = t

    def equalsPlaceholder(self,other):
        if len(self.arguments)!=len(other.arguments): return False
        i = 0
        for a in self.arguments:
            if not a.equalsPlaceholder(other.arguments[i]): return False
            i+=1
        return other==self.equalother

    def equals(self,other):
        if other.__class__ != variable: return False
        if len(self.arguments)!=len(other.arguments): return False
        if self.isEvent != other.isEvent: return False
        # if self and other both bind a variable, and bound variables are the first arguments
        # of both self and other, set those variables to be equal
        bindsVar = self.bindVar and not self.varIsConst and len(self.arguments) > 0
        other_bindsVar = other.bindVar and not other.varIsConst and len(other.arguments) > 0
        if bindsVar and other_bindsVar:
            isBinder = self.arguments[0].binder == self
            other_isBinder = other.arguments[0].binder == other
            if isBinder and other_isBinder:
                self.arguments[0].setEqualTo(other.arguments[0])
                other.arguments[0].setEqualTo(self.arguments[0])
        i = 0
        for a in self.arguments:
            if not a.equals(other.arguments[i]): return False
            i+=1
        return other==self.equalother


class lambdaExp(exp):
    def __init__(self):
        self.linkedVar = None
        self.arguments = []
        self.numArgs=0
        self.argTypes=[]
        self.parents = []
        self.isVerb=False
        self.returnType = None
        self.isNull = False
        self.posType = None
        self.inout=None
        self.doubleQuant = False
        self.name = "lam"
        pass

    # really need to go down from top
    # filling in
    def semprior(self):
        if self.funct.__class__==variable:
            return self.funct.vartopprior()
        else:
            return self.funct.semprior()

    def repairBinding(self, orig):
        if orig.var.binder == orig:
            self.var.binder = self
        self.funct.repairBinding(orig.funct)

    def isQ(self):
        return self.funct.isQ()

    def makeShell(self, expDict):
        if self in expDict:
            l = expDict[self]
        else:
            l = lambdaExp()
            v = variable(self.var)
            expDict[self.var] = v
            # self.var.setVarCopy(v)
            #print "var makeShell is ",v," for ",self.var
            l.setVar(v)
            f = self.funct.makeShell(expDict)
            l.setFunct(f)
            if self.getIsNull():
                l.setIsNull()
        return l

    def copy(self):
        #print "copying ",self.toString(True)
        #print "\n\ncopying lambda ",self
        l = lambdaExp()
        v = variable(self.var)
        self.var.setVarCopy(v)
        #print "var copy is ",v," for ",self.var
        l.setVar(v)
        l.linkedVar = self.linkedVar
        f = self.funct.copy()
        l.setFunct(f)
        if self.getIsNull(): l.setIsNull()
        return l

    def copyNoVar(self):
        l = lambdaExp()
        l.setVar(self.var)
        l.linkedVar = self.linkedVar
        f = self.funct.copyNoVar()
        if f is None: print "f is none for ",self.toString(True)
        l.setFunct(f)
        if self.getIsNull(): l.setIsNull()
        return l

    def getLvars(self):
        lvars = [self.var]
        lvars.extend(self.funct.getLvars())
        return lvars

    def isConjV(self):
        return self.funct.isConjV()

    def checkIfVerb(self):
        return self.funct.checkIfVerb()

    #IDA: only used in makePairs2()
    # this is going to pull out all nested things too.
    # def makeInOut(self):
    #     # make logical form and variable
    #     selfnew = self.copyNoVar()
    #     outargs = set()
    #     vset = set()
    #     i = 0
    #     (anew,aout,avset) = self.funct.makeInOut()
    #     if self.funct.inout==self.inout:
    #         selfnew.setArg(i,anew)
    #         outargs = outargs.union(aout)
    #         vset = vset.union(avset)
    #     else:
    #         if anew.linkedVar is not None:
    #             print "got linkedVar for ",str(id(anew)),"  in ",self.toString(True)
    #
    #             v = anew.linkedVar
    #             selfnew.funct = v
    #         else:
    #             v = variable(anew)
    #             vset.add(v)
    #             anew.linkedVar = v
    #
    #             # where do the variables go?
    #             for outarg in aout: v.addArg(outarg)
    #             selfnew.funct = v
    #             outargs.add(anew)
    #
    #
    #             lambdaord = []
    #             for outarg in aout:
    #                 v.addArg(outarg)
    #                 if outarg.linkedVar is None:
    #                     print "\n\noutarg linkedvar is none"
    #                 else:
    #                     print outarg.linkedVar.toString(True),
    #                     lambdaord.append(outarg.linkedVar)
    #             for lambdavar in reversed(lambdaord):
    #                 l = lambdaExp()
    #                 l.setVar(lambdavar)
    #                 l.setFunct(anew)
    #                 anew = l
    #
    #
    #     return (selfnew,outargs,vset)

    def compositionSplit(self,vars,compvars,ec,e):
        vargset = []
        for v in vars:
            vset = []
            for a in v.arguments: vset.append(a)
            vargset.append(vset)

        origsem = self.copy()
        #print "here and this is ",self.toString(True)
        vset = []
        self.getAllVars(vset)
        #print "this vars are"
        #for v in vset:
            #print v," ",len(v.arguments)

        newvariable = variable(ec)
        #print "newvar is ",id(newvariable)
        self.replace2(e,newvariable)
        p = self.copyNoVar()
        #print "p1 is ",p.toString(True)
        #print "ec1 is ",ec.toString(True)
        self.replace2(newvariable,e)
        #p = p.copy()
        #print "this now is ",self.toString(True)
        settype=False
        # lambdas are wrong way around
        newvars = []
        #vargset = []
        for v in vars:
            nv = variable(v)
            #print "nv is ",nv
            newvars.append(nv)
            nv.arguments = v.arguments
            ec.replace2(v,nv)
            # it is not obvious that this is right
            #vargset.append(v.arguments)
            v.arguments = []


            if v not in compvars: newvariable.addAtFrontArg(v)
            elif not settype:
                newvariable.setType(ec.type())
                settype=True

            l = lambdaExp()
            l.setFunct(ec)
            l.setVar(nv)
            ec = l

        #print "ec is ",ec.toString(True)
        #newvariable.setType(ec.type())
        #print "this now2 is ",self.toString(True)
        gotp = False
        #p = self
        while not gotp:
            if p.var in compvars:
                p = p.funct
            else: gotp = True
            if p.__class__!=lambdaExp: gotp = True
        #print "p is ",p.toString(True)
        l = lambdaExp()
        l.setFunct(p)
        l.setVar(newvariable)
        pair = (l.copy(),ec.copy())
        #print "pair from comp is ",pair[0].toString(True),"   ",pair[1].toString(True)

        #print "gonna recompose"
        l = l.copy()
        ec = ec.copy()
        # try:
        sem = l.compose(ec)
        # except AttributeError:
        #     pass
        #print "dun that"


        i = 0
        for v in vars:
            v.arguments = vargset[i]
            i+=1

        #if sem:
            #print "recomposed sem is ",sem.toString(True)
            #print "\n\ncomparing ",origsem.toString(True)," to ",sem.toString(True)
            #if sem.equals(origsem): print "same as orig"
            #else: print "not same as orig"
        #else: print "failed miserably"
        #print "\n\ncomparing ",origsem.toString(True)," to ",self.toString(True)
        #if not self.equals(origsem):
            #print "this no longer equals origsem"
        #else: print "this equals origsem"
        #print "this is ",self.toString(True)
        #print "
        vset = []
        #print "this vars are "
        #self.getAllVars(vset)
        #for v in vset:
            #print v," ",len(v.arguments)
        #vset = []
        #print "recompvars are "
        #sem.getAllVars(vset)
        #for v in vset:
            #print v," ",len(v.arguments)
        return pair

    def allSubExps(self):
        subexps = []
        subexps.append(self)
        subexps.extend(self.funct.allSubExps())
        if self.funct in subexps: subexps.remove(self.funct)
        return subexps

    def allExtractableSubExps(self):
        subexps = []
        subexps.append(self)
        subexps.extend(self.funct.allExtractableSubExps())
        if self.funct in subexps:
            subexps.remove(self.funct)
        return subexps

    def getAllVars(self,vars):
        #self.var.getAllVars(vars)
        self.funct.getAllVars(vars)

    def getheadlambdas(self):
        headlambdas = [self]
        headlambdas.extend(self.funct.getheadlambdas())
        return headlambdas

    def varsAbove(self,other,vars):
        if self==other: return
        self.funct.varsAbove(other,vars)

    def nullSem(self):
        if self.funct==self.var and len(self.funct.arguments)==0:
            return True
        return False

    def type(self):
        #print "finding type for ",self.toString(True)
        argType = self.var.type()
        #print "argType is ",argType.toString()
        functType = self.funct.type()
        #print "functType is ",functType.toString()
        t = semType(argType,functType)
        #print " pe ",t.toString()
        return t

    def getPosType(self):
        return self.funct.getPosType()

    # def isConjN(self):
    #     try:
    #         isConj = self.funct.isConjN()
    #     except AttributeError:
    #         isConj = False
    #     return isConj
        # if self.funct.__class__==conjunction:
        #     return self.funct.isConjN()
        # elif self.funct.__class__==lambdaExp:
        #     return self.funct.isConjN()
        # return False

    def setFunct(self,e):
        self.funct = e
        self.returnType = e.getReturnType()
        e.add_parent(self)
        self.argSet = True

    def setVar(self,var):
        self.var = var
        var.setBinder(self)

    def getVar(self):
        return self.var

    def getFunct(self):
        return self.funct

    def getDeepFunct(self):
        if self.funct.__class__!=lambdaExp: return self.funct
        else: return self.funct.getDeepFunct()

    def arity(self):
        return 1+self.funct.arity()

    # apply
    def apply(self,e):
        # print "trying to apply ",self.toString(True)," to ",e.toString(True)

        newExp = None
        varType = self.var.type()
        argType = e.type()
        if varType.equals(argType):
        # if self.var.type().equals(e.type()):
            for a in self.var.arguments:
                if e.__class__==variable:
                    e.addArg(a)
                else:
                    e = e.apply(a)
            if e:
                newExp = self.funct.replace2(self.var,e)
            return newExp

        #else: print self.var.type().toString()," does not equal ",e.type().toString()

    def compose(self,arg):
        if arg.__class__!=lambdaExp: return None
        #complambda = arg
        #print "composing ",self.toString(True)," with ",arg.toString(True)
        #print "gonna apply to ",arg.funct.toString(True)
        sem = self.apply(arg.funct)

        if not sem:
            sem = self.compose(arg.funct)

        if sem:
            arg.setFunct(sem)
            return arg
        else:
            return None

    def argsFilled(self):
        print "checking if args filled"
        return self.funct.argsFilled()

    # def isNounMod(self):
    #     return self.funct.isNounMod()
        #return False

    def getReturnType(self):
        return self.type()
        #.getReturnType()

    def printOut(self,top,varNum):
        print self.toString(top)

    def hasVarOrder(self,varorder):
        #if exp.varNum==0:
        #print  "checking varorder for ",self.toString(True)
        self.var.name = exp.varNum
        exp.varNum+=1
        result = self.funct.hasVarOrder(varorder)
        exp.varNum=0
        return result

    # IDA: confusing use of variables
    # def varOrder(self,L):
    #     """Omri added this. Extends L with the order of variables"""
    #     self.var.name = exp.varNum
    #     exp.varNum+=1
    #     result = self.funct.varOrder(varorder)
    #     exp.varNum=0
    #     return result

    def setArg(self,position,pred):
        self.funct.setArg(position,pred)

    def toString(self,top):
        s=""
        self.var.name = "$"+str(exp.varNum)#+"_"+str(id(self.var))
        #print "name of ",self.var," is ",self.var.name
        exp.varNum+=1
        s=s+"lambda "+self.var.name+"_{"+self.var.type().toString()+"}."+self.funct.toString(False)#+"_"+str(id(self.var))+"_{"+self.var.type().toString()+"}"+\
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            # self.clearNames()
        return s

    def toStringShell(self,top):
        s=""
        self.var.name = "$"+str(exp.varNum)#+"_"+str(id(self.var))
        #print "name of ",self.var," is ",self.var.name
        exp.varNum+=1
        s=s+"lambda "+self.var.name+"_{"+self.var.type().toString()+"}."+self.funct.toStringShell(False)#+"_"+str(id(self.var))+"_{"+self.var.type().toString()+"}"+\
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            # self.clearNames()
        return s

    def toStringUBL(self,top):
        s=""
        self.var.name = "$"+str(exp.varNum)#+"_"+str(id(self.var))
        #print "name of ",self.var," is ",self.var.name
        exp.varNum+=1
        s=s+"(lambda "+self.var.name+" "+self.var.type().toStringUBL()+" "+self.funct.toStringUBL(False)+"))"#+"_"+str(id(self.var))+"_{"+self.var.type().toString()+"}"+\
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            # self.clearNames()
        return s

    def clearNames(self):
        self.var.name=None
        self.funct.clearNames()

    def equalsPlaceholder(self,other):
        if other.__class__ != lambdaExp or \
        not other.var.equalType(self.var):
            return False
        self.var.setEqualTo(other.var)
        other.var.setEqualTo(self.var)
        return other.funct.equalsPlaceholder(self.funct)

    def equals(self,other):
        if other.__class__ != lambdaExp or \
        not other.var.equalType(self.var):
            return False
        self.var.setEqualTo(other.var)
        other.var.setEqualTo(self.var)
        return other.funct.equals(self.funct)

    def replace2(self,e1,e2):
        if self.var == e1:
            self.var = e2

        if self == e1:
            return e2
        self.funct = self.funct.replace2(e1,e2)
        return self


class eventMarker(exp):
    def __init__(self, e=None):
        self.name=None
        self.parents=[]
        self.arguments=[]
        self.isVerb=False
        self.binder = None
        self.argTypes=[]
        self.numArgs=0
        self.otherEvent = None
        self.returnType = semType.eventType()
        self.isNull = False
        self.inout = None
        self.doubleQuant = False
        if e:
            self.name=e.name

    def setBinder(self,e):
        #print "setting binder = ",e," for ",self
        self.binder = e

    def setName(self,name):
        self.name = name

    def getBinder(self):
        return self.binder

    def checkIfBound(self):
        return self.binder is not None

    def toString(self,top):
        if not self.name:
            self.name="UNBOUND"
        return self.name

    def toStringUBL(self,top):
        if not self.name:
            self.name="UNBOUND"
        return self.name

    def allSubExps(self):
        return []

    def getAllVars(self,vars):
        if not self in vars:
            vars.append(self)

    def varsAbove(self,other,vars):
        if self==other: return
        if not self in vars:
            vars.append(self)

    def clearNames(self):
        self.name=None

    def makeShell(self, expDict):
        return self

    def copy(self):
        #print "copying ",self.toString(True)
        return self

    def copyNoVar(self):
        return self

    def setOtherEvent(self,other):
        self.otherEvent = other.getEvent()
        #print "setting other event = ",other.getEvent()," for ",self

    def replace2(self,e1,e2):
        if self==e1:
            #print "replacing event ",e1," with ",e2
            return e2
        return self

    def equals(self,other):
        if other.__class__ != eventMarker:
            return False
        # always need to have set otherEvent first

        #print "trying for event, ",self
        #print "binder is ",self.binder.toString(True)
        #if self.otherEvent!=None:
            #return True
        if self.otherEvent is None:
            print "other event is None"
            print "comparing to ",other.getBinder().toString(True)," which has event ",other.getBinder().getEvent()
            if not self.binder.equals(other.getBinder()):
                return False
        # need to make sure otherEvent is set
        #if not self.binder.equals(other.getBinder()):
            #return False
        if other.__class__ != eventMarker or \
        not self.otherEvent==other:
            print "failing on event"
            print "other is ",other," otherEvent is ",self.otherEvent
            print "this is ",self
            return False
        #print "succeeding on event"
        return True

    def type(self):
        return semType.eventType()


def allcombinations(arguments,index,allcombs):
    if index == len(arguments): return
    a = arguments[index]
    newcombs = []
    for l in allcombs:
        l2 = list(l)
        l2.append(a)
        newcombs.append(l2)
    allcombs.extend(newcombs)
    allcombs.append([a])
    allcombinations(arguments,index+1,allcombs)

    
# def main(argv=None):
#     exp.main()
#
# if __name__ == "__main__":
#     main()
    
