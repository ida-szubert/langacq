from exp import *
from eventMarker import *

# predicates take a number of arguments (not fixed) and
# return a truth value
class predicate(exp):
    def setReturnType(self):
        self.returnType = semType.tType()

    def semprior(self):
        p = -1.0
        for a in self.arguments: p += a.semprior()
        return p

    def makeShell(self):
        #print "makeShelling ",self.toString(True)
        args = []
        for a in self.arguments:
            args.append(a.makeShell())
            #print "makeShell of ",a," is ",args[-1]
        e = predicate("placeholderP",self.numArgs,self.argTypes,self.posType)
        #e.hasEvent()
        i=0
        for a in args:
            e.setArg(i,a)
            i+=1
        return e

    def copy(self):
        #print "copying ",self.toString(True)
        args = []
        for a in self.arguments:
            args.append(a.copy())
            #print "copy of ",a," is ",args[-1]
        e = predicate(self.name,self.numArgs,self.argTypes,self.posType)
        e.linkedVar = self.linkedVar
        #e.hasEvent()
        i=0
        for a in args:
            e.setArg(i,a)
            i+=1
        #e.setEvent(self.getEvent())
        #if e.checkIfHaveEvent():
            #e.setEvent(self.event)
        #if self.checkIfVerb():
            #e.setIsVerb()
            ##oldevent = self.getEvent()
            ##newevent = eventMarker()
            ##e.setEvent(newevent)

            ##print "is verb so checking for top node for ",self.toString(True)
            ##t = self.top_node()
            #for p in self.parents:
                #print "replacing event in parent ",p.toString(True),oldevent,newevent
                #p.replace2(oldevent,newevent)
            #self.replace2(oldevent,newevent)
            #print ""
            #print 'copied verb, now top node is ',t.t    oString(True)
        return e

    def copyNoVar(self):
        args = []
        for a in self.arguments:
            args.append(a.copyNoVar())
        e = predicate(self.name,self.numArgs,self.argTypes,self.posType)
        e.linkedVar = self.linkedVar
        i=0
        for a in args:
            e.setArg(i,a)
            i+=1
        return e

    def setEvent(self,event):
        self.arguments[-1]=event

    def getEvent(self):
        if not self.checkIfVerb():
            return None
        if not self.arguments[-1]: return None
        if not self.arguments[-1].__class__==eventMarker: return None
        return self.arguments[-1]

    # this may need a little thinking
    def type(self):
        return semType.tType()

    def equalsPlaceholder(self,other):
        if other.__class__ != predicate or \
        (other.name!=self.name and not (("placeholderP" in self.name) or ("placeholderP" in other.name))) or \
        len(other.arguments)!=len(self.arguments):
                #print "failing in predicate ",self.toString(True),other.toString(True)
                return False
        #print "name match for ",other.name,self.name
        #if self.checkIfVerb():
            #self.getEvent().setOtherEvent(other)
            #other.getEvent().setOtherEvent(self)

        for i in range(len(self.arguments)):
            if not self.arguments[i].equalsPlaceholder(other.arguments[i]):
                return False
        return True

    def equals(self,other):
        if other.__class__ != predicate or \
        other.name!=self.name or \
        len(other.arguments)!=len(self.arguments):
            #print "failing in predicate ",self.toString(True),other.toString(True)
                return False
        #if self.checkIfVerb():
            #self.getEvent().setOtherEvent(other)
            #other.getEvent().setOtherEvent(self)
        #print "pred name match for ",other.name,self.name
        for i in range(len(self.arguments)):
            if not self.arguments[i].equals(other.arguments[i]):
                return False
        return True

    #def clearOtherEvent(self):
        #if self.checkIfVerb():
            #self.getEvent().otherEvent = None

    def toString(self,top):
        s=self.name
        #if self.checkIfVerb():
            ##self.getEvent().setName("e"+str(exp.eventNum))
            #exp.eventNum+=1

        #print "tring for ",self.name
        if len(self.arguments)>0: s=s+"("
        for a in self.arguments:
            if isinstance(a,exp): s=s+str(a.toString(False))
            if self.arguments.index(a)<self.numArgs-1: s=s+","
        if len(self.arguments)>0: s=s+")"
        #if self.event:
            #s=s+":"+self.event.toString(False)
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        #print "returning "+s
        return s

    def toStringShell(self,top):
        s="placeholderP"
        #if self.checkIfVerb():
            ##self.getEvent().setName("e"+str(exp.eventNum))
            #exp.eventNum+=1

        #print "tring for ",self.name
        if len(self.arguments)>0: s=s+"("
        for a in self.arguments:
            if isinstance(a,exp): s=s+str(a.toStringShell(False))
            if self.arguments.index(a)<self.numArgs-1: s=s+","
        if len(self.arguments)>0: s=s+")"
        #if self.event:
            #s=s+":"+self.event.toString(False)
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        #print "returning "+s
        return s

    def toStringUBL(self,top):
        s=self.name
        #if self.checkIfVerb():
            ##self.getEvent().setName("e"+str(exp.eventNum))
            #exp.eventNum+=1

        #print "tring for ",self.name
        if len(self.arguments)>0: s="("+s+str(len(self.arguments))+":t "
        for a in self.arguments:
            if isinstance(a,exp): s=s+str(a.toStringUBL(False))
            if self.arguments.index(a)<self.numArgs-1: s=s+" "
        if len(self.arguments)>0: s=s+")"
        #if self.event:
            #s=s+":"+self.event.toString(False)
        if top:
            exp.varNum = 0
            exp.eventNum = 0
            exp.emptyNum = 0
        #print "returning "+s
        return s