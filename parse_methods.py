
def combine(comp_1,comp_2,RuleSet):
	
	comb = None
	
	syn_left = comp_1[0]
	syn_right = comp_2[0]
	
	sem_left = comp_1[1]
	sem_right = comp_2[1]

	rules_left = comp_1[2]
	rules_right = comp_2[2]
	
	t = syn_left+'#####'+syn_right
	o = RuleSet.check_target(t)
	if o:
		r_head = o[0][0]
		r = [t]
		r.extend(rules_left)
		r.extend(rules_right)
		head_l_or_r = o[1] 
		if head_l_or_r == 'L':
			s1 = sem_left.copy()
			s2 = sem_right.copy()
			s_top = s1.combine(s2,False)
		elif head_l_or_r == 'R':
			s1 = sem_right.copy()
			s2 = sem_left.copy()
			s_top = s1.combine(s2,False)
		else:
			print head_l_or_r
			print 'WELL WHAT THE HELL IS H_OR_L THEN'
			abort()
		if s_top:
			comb = (r_head,s1,r)

	return comb

def cky(order,RuleSet):
	last_updated = 0
	o = {}
	parse = []
	i=0
	for item in order:
		syn_c = item[0]
		sem_c = item[1]
		o[(i,i+1)] = (syn_c,sem_c,[syn_c+'_{lex}'])
		i=i+1
	
	if len(order) == 1:
		parse.append(o[(0,1)])
		
		
	for i in range(2,len(order)+1): ## length of span
		for j in range(len(order)-i+1): ## start of span
			for k in range(1,i): ## partition of span
				if o.has_key((j,j+k)) and o.has_key((j+k,j+i)):
					comb = combine(o[(j,j+k)],o[(j+k,j+i)],RuleSet)
					if comb:
						new_syn = comb[0]
						new_sem = comb[1]
						r_used = comb[2]
						o[(j,j+i)] = comb
						if j==0 and i==len(order):
							parse.append(o[(j,j+i)])
	return parse






#
def get_parse_prob(head,lex_used,rules_used,RuleSet,lexicon):
	prob = float(1)
	#print 'rules used is ',rules_used
	
	prob = prob*RuleSet.Start_Targets.return_prob(head)
	
	for r in rules_used: #[0]:
		prob = prob*RuleSet.return_prob(r)
		
	for l in lex_used:
		syn = l[2]
		sem = l[1]
		word = l[0]
	#	if sem:
		if not sem:
			print 'null semantics in ',l
			prob = prob*lexicon.p_sem_given_syn(syn,sem)
			prob = prob*lexicon.set_word_prior(word)
		else:
			#prob = prob*lexicon.sem_model.get_prob(sem)
			prob = prob*lexicon.p_sem_given_syn(syn,sem)
			prob = prob*lexicon.p_word_given_sem_syn(word,sem,syn)
		
	return prob
#

def rep_from_sentence(sentence,RuleSet,lexicon):
	# need code from before
	lex_poss = {}
	wordset = generate_wordset(sentence,len(sentence))
	w_used = {}
	
	for level in wordset:
		for words in wordset[level]:
			for word in words:
				if not w_used.has_key(word):
					w_used[word] = lexicon.find_word(word,lexicon)

	for level in wordset:
		lex_poss[level] = []
		for words in wordset[level]:
			set1 = []
			suc = True
			for word in words:
				l_set = w_used[word]
				if l_set:
					set1.append(l_set)
				else:
					suc = False
			if suc:
				lex_poss[level].append(set1)
				
				
	no_poss = 6
	all_parses = []
	sem_used = []
	lexical_items_used = []
	parses_long = []

	for level in lex_poss:
		for part in lex_poss[level]:
			no_comb = 1
			for w in part:
				no_comb = no_comb*min(len(w),no_poss)

			parse_poss = []
			for i in range(no_comb):
				parse_poss.append([])
			n_c = no_comb
			
			for w in part:
				n = n_c/(min(len(w),no_poss))
				for i in range(no_comb):
					spot = (i/n)%(min(len(w),no_poss))
					parse_poss[i].append(w[spot])
				n_c = n_c/(min(len(w),no_poss))
			
			for p in parse_poss:
				set = []
				set2 = []
				i = 0 
				for bit in p:
					l = 1+bit[1][0].count(' ')+bit[1][0].count('\'')
					if lexicon.lex.has_key(bit[1]):
						sem_bit = lexicon.lex[bit[1]].sem.copy()
						set.append(bit[1])
					else:
						sem_bit = bit[1][1].copy()
						set.append((bit[1][0],None,bit[1][2]))
					syn_bit = bit[1][2]
					
					sem_bit.word_pos_start = i
					sem_bit.word_pos_end = i+l
					sem_bit.bottom = True
					
					i = i+l
					
					set2.append((syn_bit,sem_bit))


				parses = cky(set2,RuleSet)
	
				if parses:
					for parse in parses:
						rules_used = parse[2]
						rep = parse[1]
						head = parse[0]
						
						lex_used = set	
						
						prob = get_parse_prob(head,lex_used,rules_used,RuleSet,lexicon)
						all_parses.append((prob,lex_used,rep))		
				#else:
					#print 'parse unsuccessful for '
					#print set2
	all_parses.sort()
	all_parses.reverse()
	
	
	#for i in range(min(5 ,len(all_parses))):
		#print 'Parse ',i,' is:'
		#print all_parses[i]
		#print 'semantics are '
		#all_parses[i][2].print_self(True) 
		#print '\n\n\n'


	if len(all_parses)>1:
		for i in range(len(all_parses)):
			print 'parse ',i,' is ',all_parses[i][1],' :: prob is ',all_parses[i][0]
		
		returned_rep = all_parses[1][2]
		
		return (returned_rep,all_parses[1][1])
	else:
		return None
		





