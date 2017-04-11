from exp import *

class eventSkolem(exp):
    def __init__(self):
        self.name="ev"
        self.arguments = []
        self.numArgs=0
        self.argTypes=[]
        self.parents = []
        self.isVerb=False
        self.var = None
        self.funct = None
        self.argSet = False
        self.posType = None
        self.returnType = semType.tType()
        self.isNull = False
        self.inout = None
        self.doubleQuant = False
        pass
    # really need to go down from top
    # filling in

    def argsFilled(self):
        print "checking if args filled"
        return self.funct.argsFilled()

    def isNounMod(self):
        return False

    def copy(self):
        #print "copying ",self.toString(True)
        l = eventSkolem()
        v = eventMarker()
        #self.var.setVarCopy(v)
        l.setVar(v)
        f = self.funct.copy()
        l.setFunct(f)
        #print "going to replace var in ",l.toString(True)
        l.replace2(self.var,v)
        return l

    def copyNoVar(self):
        l = eventSkolem()
        l.setVar(self.var)
        f = self.funct.copyNoVar()
        l.setFunct(f)
        return l

    def getEvent(self):
        return self.var

    def getVar(self):
        return self.var

    def getFunct(self):
        return self.funct

    def allSubExps(self):
        subexps = [self]
        subexps.extend(self.funct.allSubExps())
        return subexps

    def allExtractableSubExps(self):
        subexps = [self]
        subexps.extend(self.funct.allExtractableSubExps())
        return subexps

    def getAllVars(self,vars):
        self.funct.getAllVars(vars)

    def varsAbove(self,other,vars):
        if self==other: return
        self.funct.varsAbove(other,vars)

    def nullSem(self):
        if self.funct==self.var and len(self.funct.arguments)==0:
            return True
        return False

    def type(self):
        return semType(semType.event,semType.t) # self.funct.type()

    def setFunct(self,exp):
        self.funct = exp
        exp.add_parent(self)
        self.argSet = True

    def setVar(self,var):
        if var.__class__!=eventMarker:
            error("Only an even can be a variable for a skolem")
        self.var = var
        var.setBinder(self)

    def addArg(self,arg):
        print "ERROR, trying to add arg to skolem"
        error("ERROR, trying to add arg to skolem")

    def getReturnType(self):
        return self.funct.getReturnType()

    def printOut(self,top,varNum):
        print self.toString(top)

    # this is a massive kludge to get around eventSkolems
    # without changing much code
    def toString(self,top):
        s=""
        #self.var.name = "e"+str(exp.varNum)
        self.var.name = "$"+str(exp.varNum)
        exp.varNum+=1
        #s=s+"sk "+self.var.name+".("+self.funct.toString(False)+")"
        s=s+"lambda "+self.var.name+"_{ev}."+self.funct.toString(False)
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s

    def toStringUBL(self,top):
        s=""
        #self.var.name = "e"+str(exp.varNum)
        self.var.name = "$"+str(exp.varNum)
        exp.varNum+=1
        #s=s+"sk "+self.var.name+".("+self.funct.toString(False)+")"
        s=s+"(lambda "+self.var.name+" ev "+self.funct.toStringUBL(False)+")"
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
        if other.__class__ != eventSkolem:
            return False
        self.var.setOtherEvent(other)
        other.var.setOtherEvent(self)
        return other.funct.equalsPlaceholder(self.funct)
    #def

    def equals(self,other):
        #print "event skolem has event ",self.var
        if other.__class__ != eventSkolem:
            return False
        self.var.setOtherEvent(other)
        other.var.setOtherEvent(self)
        return other.funct.equals(self.funct)
    #def clearOtherEvent(self):
        #self.var.clearOtherEvent()
        #self.funct.clearOtherEvent()

    def replace2(self,e1,e2):
        if self == e1:
            return e2
        if self.var == e1:
            self.var = e2
        self.funct = self.funct.replace2(e1,e2)
        return self