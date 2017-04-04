# this takes in the original childes data and adds noise
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
                    sent = line.rstrip()
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
                semDict[semLen].append((sent,sem,head))
                pass


o = open("o","w")
numSem = 3
for semLen in semDict:
    for r in range(len(semDict[semLen])):
        
        print >> o, semDict[semLen][r][0]
        print >> o, semDict[semLen][r][1]
        print >> o, semDict[semLen][r][2]
        
        print >> o,"example_end\n"
