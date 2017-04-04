# this takes in the original childes data and adds noise
import random
from errorFunct import error

charset = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
print len(charset)
charset.append('\'')
charset.append(' ')

dissallowed = ['.','!','?','[','(']
semDict = {}
for i in range(20):
    semDict[i]=[]

sent_list = []
sem_list = []
head_list = []
input_file_name = raw_input("where is the input file?\n")
numSem = int(raw_input("how many reps per example?\n"))
f = open(input_file_name,'r')
use = False
for line in f:
    if line!='':
        if line[0]!='#':
            if line.find('sent: ')!=-1:
                useSent=True
                for c in line[6:]:
                    #if not c in charset:
                    if c in dissallowed:
                        print c,'doesnt match'
                        useSent = False
                if useSent:
                    sent_list.append(line.rstrip())
                pass
            elif line.find('sem: ')!=-1 and useSent:
                sem_list.append(line.rstrip())
                sem = line.rstrip()
                semLen = line.count('(')
                pass
            elif line.find('head:')!=-1 and useSent:
                head_list.append(line.rstrip())
                head = line.rstrip()
                print 'semLen is ',semLen
                semDict[semLen].append((sem,head))
                pass

if len(sem_list)!=len(sent_list):
    error('number of LFs is not the same as number of sentences')
if len(head_list)!=len(sem_list):
    error('number of LFs is not the same as number of top nodes')

o = open(input_file_name+"."+str(numSem),"w")


for i in range(len(sent_list)):
    print >> o, sent_list[i]
    print >> o, sem_list[i]
    print >> o, head_list[i]
    semLen = sem_list[i].count('(')
    for j in range(numSem-1):
        r = random.randint(0,len(semDict[semLen])-1)
        print >> o, semDict[semLen][r][0]
        print >> o, semDict[semLen][r][1]
        
    print >> o,"example_end\n"
