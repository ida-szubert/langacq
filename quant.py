from exp import *
# from variable import variable
# from emptyExp import emptyExp

class quant(exp):
    def __init__(self,name,posType,var):
        self.linkedVar = None
        self.name=name
        self.numArgs=1
        self.var = var
        self.varIsConst = True
        self.returnType = semType.tType()
        self.nounMod = False
        if var.__class__ == variable:
            var.setBinder(self)
            self.varIsConst = False
            self.returnType = semType.eType()
            self.nounMod = True
        self.arguments=[emptyExp()]
        self.argTypes=[]
        self.parents=[]
        self.argSet=False
        #self.event = None
        self.posType = posType
        self.isVerb=False
        self.isNull = False
        #self.posType="quant"
        self.inout = None
        self.doubleQuant = False

    def semprior(self):
        return -1.0 + self.arguments[0].semprior()

    def makeShell(self):
        if self.varIsConst:
            newvar = self.var.makeShell()
        else:
            newvar = variable(None)
            self.var.setVarCopy(newvar)
        q=quant(self.name,self.posType,newvar)
        for i, a in enumerate(self.arguments):
            q.setArg(i, a.makeShell())
        # q.setArg(0,self.arguments[0].makeShell())
        return q

    def copy(self):
        #print "copying ",self.toString(True)
        if not self.varIsConst:
        # if self.var.__class__ == variable:
            newvar = variable(None)
            self.var.setVarCopy(newvar)
        else:
            newvar = self.var.copy()
        #print "newvar is ",newvar
        q=quant(self.name,self.posType,newvar)
        #print "q var is ",q.var
        for i, a in enumerate(self.arguments):
            q.setArg(i, a.copy())
        # q.setArg(0,self.arguments[0].copy())
        q.linkedVar = self.linkedVar
        #newvar = variable()
        #q.setVar(newva
        #q.replace2(self.var,newvar)
        return q

    def copyNoVar(self):
        q=quant(self.name,self.posType,self.var)
        for i, a in enumerate(self.arguments):
            q.setArg(i, a.copyNoVar())
        # q.setArg(0,self.arguments[0].copyNoVar())
        q.linkedVar = self.linkedVar
        return q

    def setArg(self,position,pred):
        if position!=0:
            if pred.__class__ == eventMarker:
                self.arguments.append(pred)
            else:
                error("only eventMarker acceptable as second arg for quant")
        if self.varIsConst:
            pred_arg = None
            for a in pred.allArgs():
                if a.equals(self.var):
                    pred_arg = a
                    break
            pred.replace2(pred_arg, self.var)
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
        for a in self.arguments:
            subExps.extend(a.allExtractableSubExps())
        return subExps

    def allSubExps(self):
        subExps = []
        subExps.append(self)
        for a in self.arguments:
            subExps.extend(a.allSubExps())
        # subExps.extend(self.arguments[0].allSubExps())
        return subExps

    def getAllVars(self,vars):
        for a in self.arguments:
            a.getAllVars(vars)
        # self.arguments[0].getAllVars(vars)

    def varsAbove(self,other,vars):
        if self==other: return
        for a in self.arguments:
            a.varsAbove(other,vars)
        # self.arguments[0].varsAbove(other,vars)

    def equalsPlaceholder(self,other):
        if other.__class__ != quant:
            answer = False
        elif self.var.__class__ != other.var.__class__:
            answer = False
        elif self.var.__class__== variable and \
                not self.var.equalType(other.var):
            answer = False
        elif not self.var.equalsPlaceholder(other.var):
            answer = False
        elif self.name!=other.name:
            answer = False
            print "quant fail"
            # return False
        elif len(self.arguments) != len(other.arguments):
            answer = False
        else:
            if self.var.__class__ == variable:
                self.var.setEqualTo(other.var)
                other.var.setEqualTo(self.var)
            # if len(self.arguments) != len(other.arguments):
            #     return False
            answer = all([a_o.equalsPlaceholder(a) for a, a_o in zip(self.arguments, other.arguments)])
        # return other.arguments[0].equalsPlaceholder(self.arguments[0])
        return answer

    def equals(self,other):
        if other.__class__ != quant:
            return False
        if self.varIsConst and other.varIsConst:
            eq_var = self.var.equals(other.var)
        elif self.varIsConst or other.varIsConst:
            eq_var = False
        else:
            eq_var = self.var.equalType(other.var)
            if eq_var:
                self.var.setEqualTo(other.var)
                other.var.setEqualTo(self.var)

        eq_pred = len(self.arguments) != len(other.arguments) and \
                  all([a_o.equalsPlaceholder(a) for a, a_o in zip(self.arguments, other.arguments)])
        # eq_pred = other.arguments[0].equals(self.arguments[0])
        eq_name = self.name==other.name
        return eq_var and eq_pred and eq_name

        # if other.__class__ != quant or \
        # not self.var.equalType(other.var) or \
        #     self.name!=other.name:
        #     print "quant fail"
        #     return False
        # self.var.setEqualTo(other.var)
        # other.var.setEqualTo(self.var)
        # return other.arguments[0].equals(self.arguments[0])

    def toStringShell(self,top):
        s=self.name
        self.var.name = "$"+str(exp.varNum)
        exp.varNum+=1
        if not self.arguments[0]: print "NONE VAR FOR ",s
        #print "quantvar is ",self.var
        s = s+"("+self.var.name
        for a in self.arguments:
            if not a.isEmpty():
                s = s+","+a.toStringShell(False)
        s += ")"
        # if not self.arguments[0].isEmpty():
        #     s=s+"("+self.var.name+","+self.arguments[0].toStringShell(False)+")"
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
        s = s+"("+self.var.name
        for a in self.arguments:
            if not a.isEmpty():
                s = s+","+a.toString(False)
        s += ")"
        # if not self.arguments[0].isEmpty():
        #     s=s+"("+self.var.name+","+self.arguments[0].toString(False)+")"
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
        s = s+"("+self.var.name
        for a in self.arguments:
            if not a.isEmpty():
                s = s+","+a.toStringUBL(False)
        s += ")"
        # if not self.arguments[0].isEmpty():
        #     s="("+s+" "+self.var.name+" "+self.arguments[0].toStringUBL(False)+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        return s

    def type(self):
        # return semType.eType()
        return self.returnType