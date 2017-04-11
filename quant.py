from exp import *
# from variable import variable
# from emptyExp import emptyExp

class quant(exp):
    def __init__(self,name,posType,var):
        self.linkedVar = None

        self.name=name
        self.numArgs=1
        self.var = var
        var.setBinder(self)
        self.arguments=[emptyExp()]
        self.argTypes=[]
        self.parents=[]
        self.argSet=False
        #self.event = None
        self.posType = posType
        self.isVerb=False
        self.returnType = semType.eType()
        self.isNull = False
        #self.posType="quant"
        self.inout = None
        self.doubleQuant = False

    def semprior(self):
        return -1.0 + self.arguments[0].semprior()

    def makeShell(self):
        newvar = variable(None)
        self.var.setVarCopy(newvar)
        q=quant(self.name,self.posType,newvar)
        q.setArg(0,self.arguments[0].makeShell())
        return q

    def copy(self):
        #print "copying ",self.toString(True)
        newvar = variable(None)
        self.var.setVarCopy(newvar)
        #print "newvar is ",newvar
        q=quant(self.name,self.posType,newvar)
        #print "q var is ",q.var
        q.setArg(0,self.arguments[0].copy())
        q.linkedVar = self.linkedVar
        #newvar = variable()
        #q.setVar(newva
        #q.replace2(self.var,newvar)
        return q

    def copyNoVar(self):
        q=quant(self.name,self.posType,self.var)
        q.setArg(0,self.arguments[0].copyNoVar())
        q.linkedVar = self.linkedVar
        return q

    def setArg(self,position,pred):
        if position!=0: error("only one arg for quant")
        self.arguments=[pred]
        self.argSet=True

    def getVar(self):
        return self.var

    def setVar(self,var):
        self.var=var
        var.setBinder(self)

    def isEntity(self):
        return True

    def allExtractableSubExps(self):
        subExps = []
        subExps.append(self)
        subExps.extend(self.arguments[0].allExtractableSubExps())
        return subExps

    def allSubExps(self):
        subExps = []
        subExps.append(self)
        subExps.extend(self.arguments[0].allSubExps())
        return subExps

    def getAllVars(self,vars):
        self.arguments[0].getAllVars(vars)

    def varsAbove(self,other,vars):
        if self==other: return
        self.arguments[0].varsAbove(other,vars)

    def equalsPlaceholder(self,other):
        if other.__class__ != quant or \
        not self.var.equalType(other.var)or \
            self.name!=other.name:
            print "quant fail"
            return False
        self.var.setEqualTo(other.var)
        other.var.setEqualTo(self.var)
        return other.arguments[0].equalsPlaceholder(self.arguments[0])

    def equals(self,other):
        if other.__class__ != quant or \
        not self.var.equalType(other.var) or \
            self.name!=other.name:
            print "quant fail"
            return False
        self.var.setEqualTo(other.var)
        other.var.setEqualTo(self.var)
        return other.arguments[0].equals(self.arguments[0])

    def toStringShell(self,top):
        s=self.name
        self.var.name = "$"+str(exp.varNum)
        exp.varNum+=1
        if not self.arguments[0]: print "NONE VAR FOR ",s
        #print "quantvar is ",self.var
        if not self.arguments[0].isEmpty():
            s=s+"("+self.var.name+","+self.arguments[0].toStringShell(False)+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        return s

    def toString(self,top):
        s=self.name
        self.var.name = "$"+str(exp.varNum)
        exp.varNum+=1
        if not self.arguments[0]: print "NONE VAR FOR ",s
        #print "quantvar is ",self.var
        if not self.arguments[0].isEmpty():
            s=s+"("+self.var.name+","+self.arguments[0].toString(False)+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        return s

    def toStringUBL(self,top):
        s=self.name.replace(":","#")
        self.var.name = "$"+str(exp.varNum)
        exp.varNum+=1
        if not self.arguments[0]: print "NONE VAR FOR ",s
        #print "quantvar is ",self.var
        if not self.arguments[0].isEmpty():
            s="("+s+" "+self.var.name+" "+self.arguments[0].toStringUBL(False)+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        return s

    def type(self):
        return semType.eType()