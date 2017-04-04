# this takes in the original childes data and adds noise
from errorFunct import error

charset = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
print len(charset)
charset.append('\'')
charset.append(' ')

dissallowed = ['.','!','?','[']
sent_list = []
sem_list = []
head_list = []
def readInFile(input_file_name):

    dissallowed = []
    sent_list = []
    sem_list = []
    head_list = []
    
    f = open(input_file_name,'r')
    use = False
    for line in f:
        if line!='':
            if line[0]!='#':
                if line.find('Sent: ')!=-1:
                    useSent=True
                    for c in line[6:]:
                    #if not c in charset:
                        if c in dissallowed:
                            print c,'doesnt match'
                            useSent = False
                    if useSent:
                        sent_list.append(line.rstrip())
                        pass
                elif line.find('Sem: ')!=-1 and useSent:
                    sem_list.append(line.rstrip())
                    pass
    return (sent_list,sem_list)


if len(sem_list)!=len(sent_list):
    error('number of LFs not the same as number of sentences')
if len(head_list)!=len(sem_list):
    error('number of LFs not the same as number of top  nodes')



def printMultiSem(of,numSem):
    o = open(of,"w")
    for i in range(len(sent_list)):
        print >> o, sent_list[i]
        k = numSem%2+1
        for j in range(k):
            print >> o,sem_list[i-j] 
        for j in range(1,numSem-k+1):
            if (i+j)<len(sent_list):
                print >> o,sem_list[i+j] 
            else:
                print >> o,sem_list[(i+j)%len(sem_list)] 
        print >> o,"example_end\n"


for i in range(1,21):
    input_file_name = "trainFiles/trainPairsBig_"+str(i)
    (sent_list,sem_list) = readInFile(input_file_name)
    numsem = 3
    output_file_name = "trainFiles/trainPairsBig"+str(numsem)+"reps_"+str(i)
    printMultiSem(output_file_name,numsem)
