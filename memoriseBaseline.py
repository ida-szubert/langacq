trainpairs = {}
for line in open("trainPairsTrain.txt"):
    if line[:5]=="Sent:": sent=line
    if line[:4]=="Sem:":
        sem = line
        trainpairs[sent] = sem
for line in open("testPairs.txt"):
    if line[:5]=="Sent:": sent=line
    if line[:4]=="Sem:":
        sem = line
        print sent
        if trainpairs.has_key(sent):
            if sem == trainpairs[sent]:
                print "CORRECT"
                print sem
                print ""
            else:
                print "WRONG"
                print sem
                print trainpairs[sent]
                print ""
        else:
            print "NO PARSE"
            
