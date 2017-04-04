


learning_rates = []
dflist = []
prodlist = []
k = 0.0001
To = 100
df = 0.0
prod = 1.0
datasize = 4000

def lam(s):
    return (1.0 - 1.0/((s-2)*k+To))


for t in reversed(range(1,datasize+1)):
    prod = 1.0
    if t<datasize: prod = prodlist[-1]*lam(t)
    prodlist.append(prod)
    if t<datasize: df = dflist[-1]+prod
    else: df = prod
    dflist.append(df)
    learning_rates.append(1.0/df)
    
    
dflist.append(df)


for j in range(1,datasize):
    df = (dflist[-1]-prodlist[j])
    dflist.append(df)
    learning_rates.append(1.0/df)

print "lr is ",learning_rates[1741]    
print "max update is ",learning_rates[1741]*datasize
