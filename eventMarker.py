from exp import *

class eventMarker(exp):
    def __init__(self):
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

    def makeShell(self):
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