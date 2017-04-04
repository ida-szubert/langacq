import sys

f = open(sys.argv[1])
seen_words = set()
new_sents = 0
tot_sents = 0
for line in f:
    tot_sents += 1
    words = line.strip().split()
    print(words)
    for w in words:
        if w not in seen_words:
            new_sents += 1
            break
    print(new_sents)
    seen_words = seen_words | set(words)

print(new_sents)
print(tot_sents)
f.close()
