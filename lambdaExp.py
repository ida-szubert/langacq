from exp import *
# from conjunction import conjunction

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

    def isQ(self):
        return self.funct.isQ()

    def makeShell(self):
        l = lambdaExp()
        v = variable(self.var)
        self.var.setVarCopy(v)
        #print "var makeShell is ",v," for ",self.var
        l.setVar(v)
        f = self.funct.makeShell()
        l.setFunct(f)
        if self.getIsNull(): l.setIsNull()
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

    # this is going to pull out all nested things too.
    def makeInOut(self):
        # make logical form and variable
        selfnew = self.copyNoVar()
        outargs = set()
        vset = set()
        i = 0
        (anew,aout,avset) = self.funct.makeInOut()
        if self.funct.inout==self.inout:
            selfnew.setArg(i,anew)
            outargs = outargs.union(aout)
            vset = vset.union(avset)
        else:
            if anew.linkedVar is not None:
                print "got linkedVar for ",str(id(anew)),"  in ",self.toString(True)

                v = anew.linkedVar
                selfnew.funct = v
            else:
                v = variable(anew)
                vset.add(v)
                anew.linkedVar = v

                # where do the variables go?
                for outarg in aout: v.addArg(outarg)
                selfnew.funct = v
                outargs.add(anew)


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


        return (selfnew,outargs,vset)

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
        sem = l.compose(ec)
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

    def isConjN(self):
        try:
            isConj = self.funct.isConjN()
        except NameError:
            isConj = False
        return isConj
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
        if self.var.type().equals(e.type()):
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

    def isNounMod(self):
        return self.funct.isNounMod()
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
            self.clearNames()
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
            self.clearNames()
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
            self.clearNames()
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