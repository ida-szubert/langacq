from exp import *

class constant(exp):
    def setReturnType(self):
        self.returnType = semType.eType()

    def type(self):
        return semType.eType()

    def makeCompNameSet(self):
        self.names = [self.name]

    def addCompName(self,n):
        self.names.append(n)
        self.names.sort()
        self.name=""
        for n in self.names:
             self.name=self.name+n
             if self.names.index(n)<len(self.names)-1:
                 self.name=self.name+"+"

    def semprior(self):
        return -1.0

    def makeShell(self):
        c = constant("placeholderC",self.numArgs,self.argTypes,self.posType)
        c.makeCompNameSet()
        return c

    def copy(self):
        #print "copying ",self.toString(True)
        c = constant(self.name,self.numArgs,self.argTypes,self.posType)
        c.makeCompNameSet()
        c.linkedVar = self.linkedVar
        return c

    def copyNoVar(self):
        c = self.copy()
        c.linkedVar = self.linkedVar
        return c

    def isEntity(self):
        return True

    def equalsPlaceholder(self,other):
        if other.__class__ != constant:
            return False
        if other.name!=self.name and not \
                (other.name=="placeholderC" or \
                     self.name=="placeholderC"):
            #print "const fail"
            return False
        return True

    def equals(self,other):
        if other.__class__ != constant:
            #print "const fail"
            #print "this is ",self.toString(True)
            #print "other is ",other.toString(True)
            #error9()
            return False
        if other.name!=self.name:
            #print "const fail"
            return False
        return True

    def addArg(self,arg):
        print "error, trying to add arg to const"
        error()

    def toStringUBL(self,top):
        n = self.name.replace(":","#")
        return n+":e"

    def toStringShell(self,top):
        return "placeholderC"