from exp import *

class eq(exp):
    def __init__(self,arg1,arg2,eqevent):
        self.linkedVar = None
        self.name = "eq"
        self.arg1=arg1
        self.arg2=arg2
        self.event = eqevent
        self.arguments=[self.arg1,self.arg2,self.event]
        self.argTypes=[self.arg1.type(),self.arg2.type(),self.event.type()]
        arg1.add_parent(self)
        arg2.add_parent(self)
        self.parents=[]
        self.numArgs=3
        self.argSet=True
        #self.event=None
        self.posType="equal"
        self.isVerb=False
        self.returnType = semType.tType()
        self.isNull = False
        self.inout = None
        self.doubleQuant = False

    def semprior(self):
        return -1.0 + self.arg1.semprior() + self.arg2.semprior()

    def makeShell(self):
        return eq(self.arg1.makeShell(),self.arg2.makeShell(),self.event.makeShell())

    def copy(self):
        e = eq(self.arg1.copy(),self.arg2.copy(),self.event.copy())
        e.linkedVar = self.linkedVar
        return e

    def copyNoVar(self):
        e = eq(self.arg1.copyNoVar(),self.arg2.copyNoVar(),self.event.copyNoVar())
        e.linkedVar = self.linkedVar
        return e

    def type(self):
        return semType.tType()

    def toString(self,top):
        s="eq("+self.arg1.toString(False)+","+self.arg2.toString(False)+","+self.event.toString(False)+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s

    def toStringShell(self,top):
        s="eq("+self.arg1.toStringShell(False)+","+self.arg2.toStringShell(False)+","+self.event.toStringShell(False)+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s

    def toStringUBL(self,top):
        s="(equals:t "+self.arg1.toStringUBL(False)+" "+self.arg2.toStringUBL(False)+" "+self.event.toStringUBL(False)+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s

    def allExtractableSubExps(self):
        subExps = []
        subExps.append(self)
        subExps.extend(self.arg1.allExtractableSubExps())
        subExps.extend(self.arg2.allExtractableSubExps())
        subExps.extend(self.event.allExtractableSubExps())
        return subExps

    def allSubExps(self):
        subExps = []
        subExps.append(self)
        subExps.extend(self.arg1.allSubExps())
        subExps.extend(self.arg2.allSubExps())
        subExps.extend(self.event.allSubExps())
        return subExps

    def getAllVars(self,vars):
        self.arg1.getAllVars(vars)
        self.arg2.getAllVars(vars)
        self.event.getAllVars(vars)

    def varsAbove(self,other,vars):
        if self==other: return
        self.arg1.varsAbove(other,vars)
        self.arg2.varsAbove(other,vars)
        self.event.varsAbove(other,vars)

    # this version returns an expression
    def replace2(self,e1,e2):
        if self == e1:
            return e2
        self.arg1=self.arg1.replace2(e1,e2)
        self.arg2=self.arg2.replace2(e1,e2)
        self.event = self.event.replace2(e1,e2)
        return self

    # this is going to pull out all nested things too.
    def makeInOut(self):
        # make logical form and variable
        selfnew = self.copyNoVar()
        outargs = set()
        vset = set()
        i = 0
        for a in [self.arg1,self.arg2]:
            (anew,aout,avset) = a.makeInOut()
            if a.inout==self.inout or a.inout is None:
                selfnew.setArg(i,anew)
                outargs = outargs.union(aout)
                vset = vset.union(avset)
            else:
                if anew.linkedVar is not None:
                    print "got linkedVar for ",str(id(anew)),"  in ",self.toString(True)
                    v = anew.linkedVar
                    selfnew.setArg(i,v)
                else:

                    v = variable(None)
                # where do the variables go?
                    for outarg in aout: v.addArg(outarg)
                    selfnew.setArg(i,v)
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
                anew.linkedVar = v
                vset.add(v)

                outargs.add(anew)
            i+=1
        return (selfnew,outargs,vset)

    def equalsPlaceholder(self,other):
        if other.__class__ != eq or \
        not other.arg1.equalsPlaceholder(self.arg1) or \
        not other.arg2.equalsPlaceholder(self.arg2):
            return False
        return True

    def equals(self,other):
        if other.__class__ != eq or \
        not other.arg1.equals(self.arg1) or \
        not other.arg2.equals(self.arg2):
            return False
        return True

    def clearParents(self):
        self.parents = []
        self.arg1.clearParents()
        self.arg2.clearParents()

    def recalcParents(self,top):
        if top:
            self.clearParents()
        self.arg1.add_parent(self)
        self.arg2.add_parent(self)
        self.arg1.recalcParents(False)
        self.arg2.recalcParents(False)