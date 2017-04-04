from random import randint
pairs = []
ex = None
for line in open("trainPairs.txt"):
    if line[:5]=="Sent:":
        if ex: pairs.append(ex)
        ex =[line]
    elif line not in ["","\n"]:
        ex.append(line)

trainout = open("trainPairsTrain.txt","w")
testout = open("testPairs.txt","w")
seenout = []
for i in range(500):
    index = randint(0,len(pairs)-1)
    seenout.append(index)
    ex = pairs[index]
    for line in ex: print >> testout, line,
    #print >> testout,"example_end\n"
    print >> testout,"example_end\n"
    
for i in range(len(pairs)):
    if i not in seenout:
        ex = pairs[i]
        for line in ex: print >> trainout, line,
        #print >> trainout,"example_end\n"
        print >> trainout,"example_end\n"

