from exp import *

class conjunction(exp):
    def __init__(self):
        self.linkedVar = None
        self.numArgs = 2
        self.arguments = [emptyExp(), emptyExp()]
        self.argTypes=[]
        self.parents = []
        self.returnType = "t"
        #self.hasEvent()
        self.posType="and"
        self.argSet=False
        self.name="and"
        self.returnType = None
        self.isNull = False
        self.inout = None
    ##
    def isConjN(self):
        isconjn = True
        for a in self.arguments:
            if not a.isNounMod():
                return False
        return True

    def isNounMod(self):
        return self.isConjN()

    def isConjV(self):
        for a in self.arguments:
            if a.checkIfVerb:
                return True
        return False

    def setType(self,name):
        self.name = name

    def type(self):
        t = None
        for a in self.arguments:
            if t and t!=a.getReturnType():
                print "bad type for conj, ",self.toString(True)," t was ",t.toString()," t now ",a.type().toString()
                return None
            else: t = a.getReturnType()
            return t

    def getPosType(self):
        t = None
        for a in self.arguments:
            if t and t!=a.getPosType():
                return None
            else:
                t = a.getPosType()
        return t

    def getReturnType(self):
        return self.type()

    def markCanBePulled(self):
        self.canbepulled = True
        for a in self.arguments:
            # a over a????
            a.canbepulled = True
            a.markCanBePulled()

    def semprior(self):
        p = -1.0
        for a in self.arguments: p += a.semprior()
        return p

    def makeShell(self):
        c = conjunction()
        c.setType(self.name)
        for i, a in enumerate(self.arguments):
        # for a in self.arguments:
            #print "gonna makeShell ",a.toString(True)
            a2 = a.makeShell()
            #print "got it ",a2.toString(True)
            c.setArg(i, a2)
            # c.addArg(a2)
        return c

    def copy(self):
        #print "copying ",self.toString(True)
        c = conjunction()
        c.linkedVar = self.linkedVar
        c.setType(self.name)
        for i, a in enumerate(self.arguments):
        # for a in self.arguments:
            #print "gonna copy ",a.toString(True)
            a2 = a.copy()
            #print "got it ",a2.toString(True)
            c.setArg(i, a2)
            # c.addArg(a2)
        return c

    def copyNoVar(self):
        c = conjunction()
        c.linkedVar = self.linkedVar
        c.setType(self.name)
        for i, a in enumerate(self.arguments):
            a2 = a.copyNoVar()
            c.setArg(i, a2)
            # c.addArg(a2)
        return c

    def addArg(self,arg):
        #if self==arg: return
        if isinstance(arg,conjunction):
            #print "here, arg is :",arg," this is :",self
            for a in arg.arguments:
                #print "a is ",a.toString(True)
                self.addArg(a)
                a.remove_parent(arg)
            return
        #print "here2, adding ",arg.toString(True)
        # self.numArgs += 1
        self.arguments.append(arg)
        arg.add_parent(self)
        self.argSet=True

        return True

    def removeArg(self,arg):
        for i in range(len(self.arguments)):
            a = self.arguments[i]
            if a==arg:
                self.arguments.pop(i)
                return

    def replace2(self,e1,e2):
        if e1==self:
            return e2
        newargset = []
        for a in self.arguments:
            newargset.append(a.replace2(e1,e2))
        # self.arguments = []
        for i, a in enumerate(newargset):
            # self.addArg(a)
            self.setArg(i, a)
        return self

    def setArg(self,position,argument):
        #error()
        #print "setting arg in ",self.toString(True)
        #print "old arg is ",self.arguments[position].toString(True),argument
        #print "new arg is ",argument.toString(True),argument
        self.arguments[position]=argument
#        self.addArg(argument)

    def checkIfVerb(self):
        for a in self.arguments:
            if a.checkIfVerb(): return True
        return False
    #def getEvent(self):
        #if self.numArgs==0: return None
        #ev = self.arguments[0].getEvent()
        #for a in self.arguments:
            #if a.getEvent()!=ev: return None
        #return ev

    def setEvent(self,event):
        for a in self.arguments:
            a.setEvent(event)
        #self.setArg(1,event)

    def isEntity(self):
        if len(self.arguments)==0: return False
        for a in self.arguments:
            if not a.isEntity(): return False
        return True

    def hasArg(self,arg):
        for a in self.arguments:
            if a.equals(arg):
                return True
        print "fail on ",arg.toString(True)
        return False

    def hasArgP(self,arg):
        for a in self.arguments:
            if a.equalsPlaceholder(arg):
                return True
        print "failP on ",arg.toString(True),"  ",self.toString(True)
        return False

    def equalsPlaceholder(self,other):
        if other.__class__!=conjunction:
            #print
            return False
        if len(self.arguments)!=len(other.arguments):
            print "conj fail1 ",len(self.arguments),len(other.arguments)," on ",self.toString(True)
            return False
        for a in self.arguments:
            if not other.hasArgP(a):
                print "conj fail on ",self.toString(True)
                print "comparing to ",other.toString(True)
                return False
        return True

    def equals(self,other):
        #self.clearOtherEvent()
        #other.clearOtherEvent()
        if other.__class__!=conjunction:
            #print
            return False
        if len(self.arguments)!=len(other.arguments):
            print "conj fail1 ",len(self.arguments),len(other.arguments)," on ",self.toString(True)
            return False
        for a in self.arguments:
            if not other.hasArg(a):
                print "conj fail on ",self.toString(True)
                print "comparing to ",other.toString(True)
                return False
        return True

    #def clearOtherEvent(self):
        #for a in self.arguments:
            #a.clearOtherEvent()

    #def allSubExps(self):
        #allsubexps = []
        ### need all combinations
        #combinations = []
        #allcombinations(self.arguments,0,combinations)
        #for combination in combinations:
            #newconj = conjunction()

            #pass
        #return []mini
    #def replace(self,e1,e2):
        ## replaces all instances of e1 with e2r
        #i=0
        #for a in self.arguments:
            #if a==e1:
                #self.arguments.remove(a)
                #self.addArg(e2)
                #for a2 in self.arguments:
                    #a2.add_parent(self)
            #else: a.replace(e1,e2)
            #i+=1

    def allExtractableSubExps(self):
        subexps = [self]
        inallsubexps = set([])
        i = 0
        for a in self.arguments:
            subexps.append(a)
            subexps.extend(a.allExtractableSubExps())
#            if i==0:
#                inallsubexps = set(a.allExtractableSubExps())
#            else:
#                inallsubexps = inallsubexps.intersection(set(a.allExtractableSubExps()))
#            i+=1
#        subexps.extend(list(inallsubexps))
#        print len(inallsubexps)," in all subexps"

        #error()
            #subexps.extend(a.allExtractableSubExps())
            # not doing across the board bullshit.
            #subexps.extend(a.allExtractableSubExps())
        return subexps

    ## this returns all splits of a conjunction
    def getconjsplits(self):
        conjsplits = []
        conjunctionorders = []
        allcombinations(self.arguments,0,conjunctionorders)
        for combination in conjunctionorders:
            inconj = conjunction()
            outconj = conjunction()
            for i, a in enumerate(self.arguments):
                if a in combination:
                    outconj.setArg(i, a.copy())
                    # outconj.addArg(a.copy())
                else:
                    inconj.setArg(i, a.copy())
                    # inconj.addArg(a.copy())
            conjsplits.append((inconj,outconj))
        return conjsplits

    def printOut(self,top,varNum):
        print self.toString(top)

    def toString(self,top):
        s="and("
        #for i in range(len(self.arguments)):
            #s=s+self.arguments[i].toString(False)
            #if i<len(self.arguments)-1: s=s+"^"
        for i in range(len(self.arguments)):
            s=s+self.arguments[i].toString(False)
            if i<len(self.arguments)-1: s=s+","
        s=s+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s

    def toStringShell(self,top):
        s="and("
        #for i in range(len(self.arguments)):
            #s=s+self.arguments[i].toString(False)
            #if i<len(self.arguments)-1: s=s+"^"
        for i in range(len(self.arguments)):
            s=s+self.arguments[i].toStringShell(False)
            if i<len(self.arguments)-1: s=s+","
        s=s+")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s

    def toStringUBL(self,top):
        s="(and "
        #for i in range(len(self.arguments)):
            #s=s+self.arguments[i].toString(False)
            #if i<len(self.arguments)-1: s=s+"^"
        for i in range(len(self.arguments)):
            s = s + self.arguments[i].toStringUBL(False)
            if i<len(self.arguments)-1:
                s = s + " "
        s = s + ")"
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
            self.clearNames()
        return s