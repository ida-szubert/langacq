from exp import *

class function(exp):
    def setReturnType(self):
        self.returnType = semType.eType()
        #self.returnType = "e"

    def isEntity(self):
        return True

    def semprior(self):
        p = -1.0
        for a in self.arguments: p += a.semprior()
        return p

    def makeShell(self):
        args = []
        for a in self.arguments:
            args.append(a.makeShell())
        e = function(self.name,self.numArgs,self.argTypes,self.posType)
        i=0
        for a in args:
            e.setArg(i,a)
            i+=1
        ##e.hasEvent()
        #e.setEvent(self.event)
        if self.checkIfVerb(): e.setIsVerb()
        return e

    def copy(self):
        #print "copying ",self.toString(True)
        args = []
        for a in self.arguments:
            args.append(a.copy())
        e = function(self.name,self.numArgs,self.argTypes,self.posType)
        i=0
        e.linkedVar = self.linkedVar
        for a in args:
            e.setArg(i,a)
            i+=1
        ##e.hasEvent()
        #e.setEvent(self.event)
        if self.checkIfVerb(): e.setIsVerb()
        return e

    def copyNoVar(self):
        args = []
        for a in self.arguments:
            args.append(a.copyNoVar())
        e = function(self.name,self.numArgs,self.argTypes,self.posType)
        e.linkedVar = self.linkedVar
        i=0
        for a in args:
            e.setArg(i,a)
            i+=1
        if self.checkIfVerb(): e.setIsVerb()
        return e

    def type(self):
        return semType.eType()

    def equalsPlaceholder(self,other):
        if other.__class__ != function or \
                (other.name!=self.name and not \
                     (other.name=="placeholderP" or self.name == "placeholderP")) or \
                     len(other.arguments) != len(self.arguments):
            print "funct fail1"
            return False
        for i in range(len(self.arguments)):
            if not other.arguments[i].equalsPlaceholder(self.arguments[i]):
                print "funct fail2"
                return False
        return True

    def equals(self,other):
        if other.__class__ != function or \
                other.name!=self.name or \
                len(other.arguments) != len(self.arguments):
            print "funct fail1"
            return False
        for i in range(len(self.arguments)):
            if not other.arguments[i].equals(self.arguments[i]):
                print "funct fail2"
                return False
        return True