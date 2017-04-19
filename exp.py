# expression, on which everything else is built
import itertools
from errorFunct import error
from semType import semType
#from cat import synCat
#from cat import cat
import copy
import random
from tools import permutations

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
        #self.event = None
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

    def isQ(self):
        return False

    def setIsVerb(self):
        self.isVerb = True

    def checkIfVerb(self):
        return self.isVerb

    def isConjV(self):
        return False

    ## from pseudocode ##
    def buildSubTree(self,pset):
        print "self is ",self.toString(True)
        newnode = self.copyNoVar()
        nout = []
        for i in range(len(self.arguments)):
            #print pset
            if pset[i][0].inout == self.inout:
                newnode.arguments[i]==pset[i][0]
                if pset[i][1] is not None:
                    nout.extend(pset[i][1])
            else:
                v = variable(None)
                a = pset[i][0]
                for k in range(len(pset[i][1])):
                    if pset[i][1][k]!=pset[i][1][k].linkedVar:
                        u = pset[i][1][k].linkedVar
                        v.addArg(pset[i][1][k])
                        al = lambdaExp()
                        al.setVar(u)
                        al.setFunct(a)
                        a = al
                v.arguments.reverse()
                a = a.copyNoVar()
                nout.append(a)
                v.setType(a.type())
                a.linkedVar = v
                newnode.setArg(i,v)

        return (newnode,nout)

    def buildAllSubTrees(self):
        nodename = self
        Q = [] #[])
        nodeout = []
        if len(nodename.arguments)==0 and self.__class__!=lambdaExp:
            print "args and that shit"
            print nodename.toString(True)
            if nodename.__class__ == variable:
                nodename.inout=nodename.binder.inout
                nodename.linkedVar = nodename
                Q.append((nodename,[nodename]))
                return Q
            newnode = nodename.copyNoVar()
            newnode.inout = True
            Q.append((newnode,nodeout))
            newnode = nodename.copyNoVar()
            newnode.inout = False
            Q.append((newnode,nodeout))
        elif self.__class__==conjunction:
            newnode = nodename.copyNoVar()
            Q.append((newnode,[]))
        elif self.__class__==lambdaExp:
            return self.funct.buildAllSubTrees()
        else:
            A = []
            for i in range(len(nodename.arguments)):
                print "here innit"
                nodename.arguments[i].inout = None
                A.append(nodename.arguments[i].buildAllSubTrees())
            print "A is ",A
            for B in list(itertools.product(*A)):
                print "B is ",B
                if nodename.inout is None:
                    newnode = nodename.copyNoVar()
                    newnode.inout = True
                    (newnode,nodeout) = newnode.buildSubTree(B)
                    if len(nodeout)>2: continue
                    qseen = []
                    for l in list(itertools.permutations(nodeout)):
                        if (newnode,l) in qseen:
                            print "seen qperm "
                        qseen.append((newnode,l))

                        Q.append((newnode,l))
                newnode = nodename.copyNoVar()
                newnode.inout = False
                (newnode,nodeout) = newnode.buildSubTree(B)
                if (newnode,nodeout) in Q:
                    print "duplicating in Q ",newnode.toString(True)
                Q.append((newnode,nodeout))

        print "Q is ",Q
        qseen = []
        Q2 = []
        for q in Q:
            print "q is ",q
            if q[0].toString(True) in qseen:
                print "duplicated in q ",q, q[0].toString(True)
                for a in q[1]: print a.toString(True)
            else:
               Q2.append(q) 
            qseen.append(q[0].toString(True))
        return Q2

    def genAllSplits(self):
        print "deffo here"
        pairsseen = []
        for node in self.allExtractableSubExps():
            for e in self.allExtractableSubExps():
                if not e in node.allExtractableSubExps():
                    e.inout = True
            print "node is ",node.toString(True)
            node.inout = False
            seena = []
            for (a,aout) in node.buildAllSubTrees():

                v = variable(None)
                print "aout is ",aout
                print "before doing lambdas a is ",a.toString(True)
                for k in range(len(aout)):
                    v.arguments.append(aout[k])
                    u = aout[k].linkedVar
                    al = lambdaExp()
                    print "funct is ",aout[k].toString(True)
                    print "u is ",u
                    if u:
                        al.setVar(u)
                        al.setFunct(a)
                        a = al
                    else:
                        print "none u for ",aout[k].toString(True)
                v.arguments.reverse()
                v.setType(a.type())
                if a.toString(True) in seena:
                    print "duplicated a ",a.toString(True)
                else:
                    print "orig a ",a.toString(True)
                seena.append(a.toString(True))
                if node.__class__==lambdaExp:
                    origthing = node.getDeepFunct()
                    print "deep funct"
                    f = self.replace2(node.getDeepFunct(),v)

                else:
                    f = self.replace2(node,v)
                    origthing = node
                fl = lambdaExp()
                fl.setFunct(f)
                fl.setVar(v)
                print "\n"
                print "a is ",a.toString(True)
                print "f is ",fl.toString(True)
                if (fl.toString(True),a.toString(True)) in pairsseen:
                    print "duplicated pair"
                print "pair is ",fl.toString(True)," ",a.toString(True)
                pairsseen.append((fl.toString(True),a.toString(True)))
                pair = ((fl.copy(),a.copy()))
                f = self.replace2(v,origthing)
                print "self back to ",self.toString(True)

                self.resetLinkedVar()
                self.resetInOut()

            
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

    def isNounMod(self):
        return self.nounMod
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
        error()
        ## need to change for binders
        #return self.copy()

    def copy(self):
        print "copying ",self.toString(True)
        error()

    def makeShell(self):
        error()
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

    def missingArg(self,position):
        if position>=self.numArgs:
            return False
        if self.arguments[position].isEmpty(): return True
        return False

    def hasFilledArg(self,position):
        if position>=self.numArgs:
            return False
        if self.arguments[position].isEmpty(): return False
        return True

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
        
    def resetEqualOther(self):
        for e in self.allSubExps():
            if e.__class__ == variable:
                e.equalother = None
        
    def resetLinkedVar(self):
        for e in self.allSubExps():
            e.linkedVar = None
        vset = []
        e.getAllVars(vset)
        for v in vset:
            v.linkedVar = None
        
    def resetInOut(self):
        for e in self.allSubExps():
            e.inout = None
        vset = []
        e.getAllVars(vset)
        for v in vset:
            v.inout = None

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
        
    def makeTree(self,inNodes,outNodes):
        pass
    
    def allTrees(self):
        selfTrees = []
        selfTrees.append(self)
        argTrees = []
        for a in self.arguments:
            argTrees.append(a.allTrees())
            
        combs = getCombs(argTrees)
        return selfTrees

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
        for e in self.allSubExps():
            if e.__class__ in [lambdaExp,quant,eventSkolem]:
                boundVars.append(e.var)
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
            for a in v.arguments: vset.append(a)
            vargset.append(vset)
            
        
        # first of all, make function application
        origsem = self.copy()
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
            if vars[varindex] == self.var and \
				            vars[varindex] not in abovevars and \
				            vars[varindex].__class__!=eventMarker:
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

        sem = l1.apply(e1)
        if not sem.equals(self):
            print "sems dont match : "+sem.toString(True)+"  "+self.toString(True)
        
        if not self.equals(origsem):
            print "\nnot back to orig"
            print self.toString(True)
            print origsem.toString(True)
            print ""
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
        
        
    def split(self,e):
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
    
    def getheadlambdas(self):
        return []
    
    def markCanBePulled(self):
        for e in self.allSubExps():
            pass

    def getCanBePulled(self):
        pass

    def setInOut(self,inout):
        self.inout = inout

    def setInOuts(self):
        for e in self.allSubExps():
            if e==self: continue
            inout = random.random()>0.5
            e.setInOut(inout)

    # this is going to pull out all nested things too.
    # make 
    def makeInOut(self):
        # make logical form and variable 
        selfnew = self.copyNoVar()
        outargs = set()
        vset = set()
        i = 0
        for a in self.arguments:
            (anew,aout,avset) = a.makeInOut()
            print "dealing with arg ",i," which gives ",anew.toString(True)," in ",self.toString(True)
            print "dealing with arg ",str(id(a))," in ",self.toString(True)

            print "a.inout = ",a.inout," this inout = ",self.inout
            if a.inout==self.inout or a.inout is None:
                print "selfnewnow is ",selfnew.toString(True)
                print "len args is ",len(selfnew.arguments)
                print "i is ",i
                print "anew is ",anew.toString(True)
                selfnew.setArg(i,anew)
                print "selfnewnow is ",selfnew.toString(True)
                #outargs.extend(aout)
                #vset.extend(avset)
                outargs = outargs.union(aout)
                vset = vset.union(avset)
            else:
                if anew.linkedVar is not None:
                    print "got linkedVar for ",anew.toString(True),str(id(anew)),"  in ",self.toString(True)
                    v = anew.linkedVar
                    selfnew.setArg(i,v)
                else:
                
                    v = variable(None)
                    print "making var for ",anew.toString(False)#," but have variables ",
                    print "setting new arg in ",selfnew.toString(True)
                    
                    selfnew.setArg(i,v)
                    print "now is ",selfnew.toString(True)
                    # where do the variables go?
                    lambdaord = []
                    for outarg in aout:
                        v.addArg(outarg)
                        if outarg.linkedVar is None:
                            print "\n\noutarg linkedvar is none"
                        else: 
                            print outarg.linkedVar.toString(True),
                            lambdaord.append(outarg.linkedVar)
                    for lambdavar in reversed(lambdaord):
                        l = lambdaExp()
                        l.setVar(lambdavar)
                        l.setFunct(anew)
                        anew = l

                    v.setType(anew.type())
                    print "setting linkedVar for ",anew.toString(True)
                    anew.linkedVar = v
                    vset.add(v)

                print " anew now is ",anew.toString(True)
                # for outv in avset:
                print "\n\n"
                outargs.add(anew)
            i+=1
        return (selfnew,outargs,vset)

    def makeSplit(self,undere):
        eorig = self.copy()
        print "\n\nundere is ",undere.toString(True)
        if undere.__class__ == lambdaExp: return None
        if self.__class__ == lambdaExp and undere==self.funct: return None
        
        selfnew = self.copy()
        (anew,outs,vset) = undere.makeInOut()

        v = variable(anew)
        lambdaord = []
        for a in outs:
            print "aout is ",a.toString(True),a
            v.addArg(a)
            lambdaord.append(a.linkedVar)
        print "lambdaord is ",len(lambdaord)," long"
        for lambdavar in reversed(lambdaord):
            l = lambdaExp()
            l.setVar(lambdavar)
            l.setFunct(anew)
            anew = l
            # REALLY NEED TO MATCH VARIABLE ORDER TO ARG
            # ORDER AND LAMBDA ORDER
        print "v is ",id(v)
        v.setType(anew.type())
        print "self before replace is ",self.toString(True)
        print "undere is ",undere.toString(True)
        self.replace2(undere,v)
        print "self is ",self.toString(True)
        enew = self.copyNoVar()
        
        l = lambdaExp()
        l.setVar(v)
        l.setFunct(enew)
        print "l is ",l.toString(True)
        enew = l.copy()
        
        print "pairMS is ",enew.toString(True),anew.toString(True)
        pair = (enew.copy(),anew.copy())
        eback = enew.apply(anew)
        self.replace2(v,undere)
        print "self back to ",self.toString(True)
        if eback:
            print "enew back to ",eback.toString(True)
            eback.resetEqualOther()
            eorig.resetEqualOther()
            eback.resetLinkedVar()
            eorig.resetLinkedVar()
            eback.resetInOut()
            eorig.resetInOut()

            if not eback.equals(eorig):
                print "got enew but not back to orig ",eback.toString(True)
            else:
                print "equals orig"
        else:
            print "enew back to None"
            self.replace2(v,undere)
            print "eback to ",self.toString(True)
            if not eorig.equals(self):
                print "not back to orig"
            print "******* DONE *********"
        print "returning ",pair
        return pair

        # v = variable(anew)
        # for a in outs:
        #     print "aout is ",a.toString(True),a
        #     v.addArg(a)
        #
        # # REALLY NEED TO MATCH VARIABLE ORDER TO ARG
        # # ORDER AND LAMBDA ORDER
        #
        # print "a1 is ",anew.toString(True)
        # print "e is ",self.toString(True)
        #
        # # do not want to do this
        # self.replace2(undere,v)
        # for av in vset:
        #     l = lambdaExp()
        #     l.setVar(av)
        #     l.setFunct(anew)
        #     anew = l
        #
        #
        #
        # print "Anew is ",anew.toString(True)
        # #    print "Vnew is ",v.toString(True)
        #
        # enew = self.copyNoVar()
        # l = lambdaExp()
        # l.setVar(v)
        # l.setFunct(enew)
        # enew = l.copy()
        #
        # print "here ENew is ",enew.toString(False)
        # self.replace2(v,undere)
        # print "self back to ",self.toString(True)
        # return (enew,anew)

    def makePairs2(self,depth=1):
        if depth>6: return
        depth = depth+1
        pairs = []
        print "splitting ",self.toString(True)
        seentypes = []
        conjunctions = []
        numsplits = 0
        print "self in makepairs 2 is ",self.toString(True)
        subExps = self.allExtractableSubExps()
        for e in subExps:
            if e == self: continue
            nu = 0
            print "e is ",e.toString(True)
            for e2 in e.allExtractableSubExps():
                if e2 == e: continue 
                if e2.__class__==variable: continue
                # not sure that we have a decent thing going 
                # on with return type but that can be fixed 
                nu += 1
            numsplits += pow(2,nu)
            for i in range(pow(2,nu)):
                e.resetBinders()
                for unune in e.allSubExps():
                    unune.linkedVar = None
                    print "setting to false for ",unune.toString(True)
                    unune.setInOut(False)

                bi = list(bin(i)[2:])
                # need to pack bi with zeroes
                for j in range(len(bi),nu): bi.insert(0,0)
                print "bi is ",bin(numsplits)[2:]
                j = 0
                for e2 in e.allExtractableSubExps():
                    if e2 == e: continue 
                    if e2.__class__==variable: continue

                    print "e2 is ",e2.toString(True)
                    if  bi[j]==0:  e2.setInOut(False)
                    else: e2.setInOut(True)
                    j+=1
                vset = []
                e.getAllVars(vset)
                for v in vset: v.setVarInOut()

                pair = self.makeSplit(e)
                if pair and pair[0] and pair[1]:
#                    pair[0].makePairs2()
#                    pair[1].makePairs2()
#                print "made pair, self is ",self.toString(True)
                    pairs.append((pair[0].copy(),pair[1].copy(),0,0,0))
#                    pairs[-1][0].makePairs2(depth)                
#                    pairs[-1][1].makePairs2(depth)
                if pair is not None:
                    print "i is ",i," bi is ",bi,"pair is ",pair[0].toString(True),pair[1].toString(True)
                    print "pair is ",pair[0].toString(True),pair[1].toString(True)

            print "numsplits i= ",numsplits
        return pairs

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
            if e.__class__==conjunction:
                #print e.toString(True)," is a conjunction"
                conjunctions.append(e)
            #else:
            repPairs.extend(self.split(e))
            
            #repPairs.extend
            
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
    
    @staticmethod
    def main():

        r1 = exp.makeExpWithArgs("lambda $0_{e}.lambda $1_{ev}.and(aux|be&PRES(part|do-PROG(pro|you,$0,$1),$1),prep|in(det|that($2,n|placeholderP($2)),$1))",{})
        r2 = exp.makeExpWithArgs("lambda $0_{ev}.not(and(aux|do(and(v|want(pro|I,pro|you,$0),v|trip(pro|I,$0)),$0),prep|on(pro:poss:det|your($1,n|shoelace($1)),$0)),$0)",{});
        r3 = exp.makeExpWithArgs("lambda $0_{ev}.Q(aux|do&PAST(v|find(pro|you,det|the($1,and(adj|little($1),adj|red($1),n|bicycle($1))),$0),$0),$0)",{})
        r4 = exp.makeExpWithArgs("lambda $0_{ev}.aux|be&3S(and(part|go-PROG(pro|she,$0),v|have(pro|she,det|a($1,n|bottle($1)),$0)),$0)",{});
        r4 = exp.makeExpWithArgs("lambda $0_{ev}.not(and(aux|do(and(v|want(pro|I,pro|you,$0),v|trip(pro|I,$0)),$0),prep|on(pro:poss:det|your($1,n|shoelace($1)),$0)),$0)",{})

        print "made reps"
        e1 = r1[0]
        e2 = r2[0]
        print e1.equals(e2)
        print e1.equalsPlaceholder(e2)
        e = e2
        print "\n\nmade exp"
        e.printOut(True,0)
        eorig = e.copy()
        e4 = r4[0]
        b = e4.makePairs()

        e4.genAllSplits()

        return
        a = e4.makePairs2()
        print "makepairs2 DONE\n\n\n"

        for p in a:
            print "pair2",p[0].toString(True),p[1].toString(True)
        print len(a), " from makepairs2"
        return 

        print "\nExp Splits are:"
        for split in e.makePairs():
            print split[0].toString(True)," ",split[1].toString(True)
        print "\n\n\n\n"
        i = 0
        for undere in e.allSubExps():
            if undere.__class__==variable: continue
            print "e now is ",e.toString(True) 
            e.resetBinders()
            for unune in e.allSubExps():
                unune.linkedVar = None 
                print "setting to false for ",unune.toString(True)
                unune.setInOut(False)
            print "\n\nundere is ",undere.toString(True)
            if undere.__class__ == lambdaExp: continue
            if e.__class__ == lambdaExp and undere==e.funct: continue
            undere.setInOut(True)

            undere.setInOuts()
            vset = []
            e.getAllVars(vset)
            for v in vset: v.setVarInOut()
            selfnew = e.copy()
            print "making inout"
            (anew,outs,vset) = undere.makeInOut()
            print "made inout"
            print "ANEW WITH LAMBDA IS ",anew.toString(True)
            v = variable(anew)
            lambdaord = []
            for a in outs:
                print "aout is ",a.toString(True),a
                v.addArg(a)
                lambdaord.append(a.linkedVar)
            for lambdavar in reversed(lambdaord):
                l = lambdaExp()
                l.setVar(lambdavar)
                l.setFunct(anew)
                anew = l
            # REALLY NEED TO MATCH VARIABLE ORDER TO ARG
            # ORDER AND LAMBDA ORDER
            v.setType(anew.type())

            print "a1 is ",anew.toString(True)
            print "e is ",e.toString(True)

            e.replace2(undere,v)

            print "Anew is ",anew.toString(True)
            print "e1 is ",e.toString(True)            

            enew = e.copyNoVar()
            print "enew1 is ",enew.toString(True)
            l = lambdaExp()
            l.setVar(v)
            l.setFunct(enew)

            enew = l.copy()

            print "here2 ENew is ",enew.toString(False)
            print "pair is ",enew.toString(True),anew.toString(True)
            
            eback = enew.apply(anew)

            if eback:
                print "enew back to ",eback.toString(True)
                eback.resetEqualOther()
                eorig.resetEqualOther()
                if not eback.equals(eorig):
                    print "got enew but not back to orig ",eback.toString(True)
                else:
                    print "equals orig"
            else:
                print "enew back to None"
            e.replace2(v,undere)
            print "eback to ",e.toString(True)
            if not eorig.equals(e):
                print "not back to orig"
            print "******* DONE *********"


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

    def makeShell(self):
        return emptyExp()

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
            self.clearNames()
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
            self.clearNames()
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
        if e:
            self.t = e.type()
            self.numArgs = e.numArgs
            self.argTypes = e.argTypes
            #self.arguments = []
            #for a in e.arguments:
                #print "adding arg ",a
                #self.addAtFrontArg(a)
            #self.arguments = e.arguments
            self.returnType = e.getReturnType()

        else:
            self.numArgs = 0
            self.argTypes = []
            self.arguments = []
            # assume that we only introduce entity
            # vars from the corpus
            #self.returnType = "e"
            self.returnType = semType.eType()
            self.t = semType.eType()
        self.isNull = False

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

    def makeShell(self):
        if self.varcopy is None: return None
        args = []
        for a in self.arguments:
            args.append(a.makeShell())
        v = self.varcopy
        v.arguments = args
        return v

    def isEmpty(self):
        return False

    def isConjN(self):
        return False

    def copy(self):
        if self.varcopy is None:
            return None
        args = []
        for a in self.arguments:
            args.append(a.copy())
        v = self.varcopy
        v.linkedVar = self.linkedVar
        v.arguments = args
        return v

    def copyNoVar(self):
        return self

    def allSubExps(self):
        subexps = [self]
        if len(self.arguments)>0:
            subexps.append(self)
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
            self.clearNames()
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
            self.clearNames()
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
        if len(self.arguments)!=len(other.arguments): return False
        i = 0
        for a in self.arguments:
            if not a.equals(other.arguments[i]): return False
            i+=1
        return other==self.equalother


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

    
def main(argv=None):
    exp.main()

if __name__ == "__main__":
    main()
    
