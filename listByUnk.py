words = {}
sents = {}
for i in range(10):
    sents[i]=[]
sentcount = 0
for line in open("trainPairs.txt","r"):
    if line[:5]!="Sent:": continue
    unk = 0
    unks = []
    for w in line.split():
        if not words.has_key(w):
            unk += 1
            unks.append(w)
            words[w]=w
    sentcount+=1
    sents[unk].append((sentcount,line,unks))

#for i in range(10):
#    print sents[i]

for i in sents[2]: print i
