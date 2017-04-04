# this has all the functions used to translate the dependency graphs


def srl(semantics,root_sem):
	subj = None
	for node in semantics:
		if node.ty == 'SRL':
			if len(node.parents)==1:
				if semantics[node.parents[0]].pos == 'v':
					father = node.parents[0]
					# cut link from v->srl
					semantics[father].remove_dependent(node.position,semantics)
					subj = node.find_dep_type('SUBJ',semantics)
					subj3 = semantics[father].find_dep_type('SUBJ',semantics)
					# for all parents of the v
					if len(semantics[father].parents)>0:
						for parent in semantics[father].parents:
							# flip dependent
							semantics[parent].remove_dependent(father,semantics)
							semantics[parent].add_dependent(node.position,'SRL',semantics)
					# make srl parent of v
					node.add_dependent(father,'???',semantics)
					if subj and subj3:
						print 'SRL ERROR - 2 subj'
					elif subj:
						# give v subj - but set it as shadow
						semantics[father].add_dependent(subj.position,'SUBJ',semantics)
						subj2 = semantics[father].find_dep_type('SUBJ',semantics)
						subj2.set_shadow()
					elif subj3:
						node.add_dependent(subj3.position,'SUBJ',semantics)
						subj3.set_shadow()
					if len(node.parents)==1:
						# maybe there are two verbs???
						print "2 v??"
						subj = semantics[node.parents[0]].find_dep_type('SUBJ',semantics)
						if subj:
							if len(node.dependents)==1:
								if semantics[node.dependents[0].position].pos == 'v':
									semantics[node.dependents[0].position].add_dependent(subj.position,'SUBJ',semantics)
									subj2 = semantics[node.dependents[0].position].find_dep_type('SUBJ',semantics)
									subj2.set_shadow()
							node.add_dependent(subj.position,'SUBJ',semantics)
							subj2 = node.find_dep_type('SUBJ',semantics)
							subj2.set_shadow()
						
						
					
					if father == root_sem.position:
						root_sem = node
					#print 'done srl'
				#else: print 'not verb - srl'
	return root_sem
		
	
		

def aux(semantics,root_sem):
	for node in semantics:
		if node.ty == 'AUX': # might want to consider using the name 'aux' instead of type
			if len(node.parents)==1 and (semantics[node.parents[0]].pos=='v' or semantics[node.parents[0]].pos=='part'):
				subj = semantics[node.parents[0]].find_dep_type('SUBJ',semantics)
				subj2 = node.find_dep_type('SUBJ',semantics)
				if subj2: print 'aux subj2'
				## this happens just a few times - mainly towards the end of the input
				
				
				
				## unlike for CPZR the positions are not flipped but AUX is moved out 
				## of the verb parent taking its dependents with it
				father = node.parents[0]
				semantics[father].remove_dependent(node.position,semantics)
				#if semantics[father].find_dep('wh',semantics):
				wh = semantics[father].find_dep('wh',semantics)
				if not wh: 
					wh = node.find_dep('wh',semantics)
				if wh:
					print 'wh - aux'
					if semantics[wh.position].ty == 'PRED' or semantics[wh.position].ty == 'OBJ':
						print 'is predobj in aux'
					elif semantics[wh.position].ty == 'SUBJ':
						print 'subj in aux'
						
					else:
						print 'not predobj - is ', semantics[wh.position].ty
	
	####################################################
	## NEED TO CHANGE THIS!!!!!!!!!!!		  ##
	####################################################
					subj = False
	####################################################
	####################################################
					
					if semantics[wh.position].dependents!=[]:
							print 'wh dep error'
					wh_father = semantics[wh.position].parents[0]
					#wh.set_shadow()
					semantics[wh_father].remove_dependent(wh.position,semantics)
					semantics[wh.position].add_dependent(node.position,'AUX',semantics)
					#print 'wh - aux'
					
					
				if len(semantics[father].parents)>0:
					if not wh:
						for parent in semantics[father].parents:
							semantics[parent].remove_dependent(father,semantics)
							semantics[parent].add_dependent(node.position,'AUX',semantics)
					else:
						# this is a wh question add all pointers to the 
						for parent in semantics[father].parents:
							semantics[parent].remove_dependent(father,semantics)
							semantics[parent].add_dependent(wh.position,'WH',semantics)
						if semantics[semantics[wh.position].parents[0]].pos == 'aux':
							root_sem = flip_parent(semantics,semantics[wh.position],root_sem)
				
				node.add_dependent(father,'???',semantics)
				if subj:
					node.add_dependent(subj.position,'SUBJ',semantics)
					subj.set_shadow()
				else:
					print 'aux - no subj'
				if father == root_sem.position and not wh:
					root_sem = node
				elif  father == root_sem.position and wh:
					root_sem = semantics[wh.position]
					
	return root_sem


def exchange_parent(semantics,node,root_sem):
	father = node.parents[0]
	semantics[father].remove_dependent(node.position,semantics)
	if len(semantics[father].parents)>0:
		for parent in semantics[father].parents:
			semantics[parent].remove_dependent(father,semantics)
			semantics[parent].add_dependent(node.position,'???',semantics)
	for dep in semantics[father].dependents:
		semantics[father].remove_dependent(dep.position,semantics)
		node.add_dependent(dep.position,'???',semantics)
	node.add_dependent(father,'???',semantics)
	if father == root_sem.position:
		root_sem = node
	return root_sem


def flip_parent(semantics,node,root_sem):
	## this flips the positions of a parent child relationship
	print "from top"
	father = node.parents[0]
	semantics[father].remove_dependent(node.position,semantics)
	if len(semantics[father].parents)>0:
		for parent in semantics[father].parents:
			semantics[parent].remove_dependent(father,semantics)
			semantics[parent].add_dependent(node.position,'AUX',semantics)
	if semantics[father]==node: return root_sem
	if len(node.dependents)>0:
		for dep in node.dependents:
			semantics[father].add_dependent(dep.position,'???',semantics)
			print "added dep  "+str(dep.position)
			print node.dependents
	node.dependents = []
	node.add_dependent(father,'???',semantics)
	if father == root_sem.position:
		root_sem = node
	return root_sem			

def move_cpzr(node,semantics,root_sem,moved_out_of_verb):
	## cpzr should be moved to the head of the verb that contains it and should also go in front of aux BUT it shouldn't muove all the way up the verb chain
	
	if moved_out_of_verb:
		if len(node.parents)==1 and semantics[node.parents[0]].pos=='aux':
			root_sem = flip_parent(semantics,node,root_sem)
	
	else:
		if len(node.parents)==1 and (semantics[node.parents[0]].pos=='v' or semantics[node.parents[0]].pos=='part'):
			root_sem = flip_parent(semantics,node,root_sem)
			if len(node.parents)>0:
				root_sem = move_cpzr(node,semantics,root_sem,True)
		
		
		elif len(node.parents)==1 and semantics[node.parents[0]].pos=='aux':
			root_sem = flip_parent(semantics,node,root_sem)
		
		
		elif len(node.parents)==1:
			root_sem = flip_parent(semantics,node,root_sem)
			if len(node.parents)>0:
				root_sem = move_cpzr(node,semantics,root_sem,False)
		
		
		#elif len(node.parents)!=1:
			#print 'not one parent ',node.parents
			
	return root_sem

## CPZR is moved to head the verb and then if there is an aux it can head that too

def cpzr(semantics,root_sem):
	for node in semantics:
		if node.ty == 'CPZR':
			root_sem = move_cpzr(node,semantics,root_sem,False)
	return root_sem


def conj(semantics,root_sem):
	## conj should NEVER have more than 2 dependents unless they are COM or VOC
	for node in semantics:
		if node.name.find('conj:coo')!=-1: #looks for 'and' and 'but'
			if len(node.dependents)==2:
				print 'correct number of coords'
				if semantics[node.dependents[0].position].pos!=semantics[node.dependents[1].position].pos:
					if (semantics[node.dependents[0].position].pos == 'v' or semantics[node.dependents[0].position].pos == 'aux' or semantics[node.dependents[0].position].pos == 'part') and (semantics[node.dependents[1].position].pos == 'v' or semantics[node.dependents[1].position].pos == 'aux' or semantics[node.dependents[1].position].pos == 'part'):
						#print 'actually match'
						pass
					else:
						#print 'mismatched coords'
						pass
			elif len(node.dependents)>2:
				print 'more than 2 dependents'
				#print 'conjunction with not 2 dependents'
				#print len(node.dependents)
				pass
			
			
	return root_sem
	## look at dependents - are they the same?
	## if not bring aux/cpzr out

def neg(semantics,root_sem):
	for node in semantics:
		## this is 	WAY too simplistic - still the way that they have
		## dealt with negation makes you wonder why they even
		## bothered annotating this stuff in the first place
		if len(node.parents)==1 and node.ty == 'NEG':
			root_sem = flip_parent(semantics,node,root_sem)
	return root_sem
		
		
def inf(semantics,root_sem):
	for node in semantics:
		if len(node.parents) == 1 and node.ty == 'INF':
			if semantics[node.parents[0]].pos == 'v': #or semantics[node.parents[0]].pos == 'part':
				root_sem = flip_parent(semantics,node,root_sem)
				## parent only 
				pass
			elif semantics[node.parents[0]].pos == 'part':
				pass
				## only happens once - ignore
				#print 'part parent - should we shift?'
			if len(node.dependents)!=1:
				print 'error - inf deps'
			else:
				if semantics[node.dependents[0].position].pos == 'v' and len(node.parents)==1:
					print node.parents[0]
					subj = semantics[node.parents[0]].find_dep_type('SUBJ',semantics)
					if subj is None:
						print 'error - inf subj'
					else:
						 semantics[node.dependents[0].position].add_dependent(subj.position,'SUBJ',semantics)
						 subj2 = semantics[node.dependents[0].position].find_dep_type('SUBJ',semantics)
						 subj2.set_shadow()
	return root_sem
		


def det(semantics,root_sem,flipped):
	for node in semantics:
		if node.ty == 'DET':
			if len(node.parents)!=1:
				if not node == root_sem:
					print 'ERROR - NOT ONE PARENT 229'
			else:
				if semantics[node.parents[0]].pos == 'n' or  semantics[node.parents[0]].pos == 'n:pt' or semantics[node.parents[0]].pos == 'pro:indef' or semantics[node.parents[0]].pos == 'det:num' or semantics[node.parents[0]].pos == 'n:adj' or semantics[node.parents[0]].pos == 'adj'  or semantics[node.parents[0]].pos == 'n:v' or semantics[node.parents[0]].pos == 'n:prop' or semantics[node.parents[0]].pos == 'on' or semantics[node.parents[0]].pos == 'n:let':
					## pro:wh ??????
					## have a what?
					root_sem = flip_parent(semantics,node,root_sem)
				elif semantics[node.parents[0]].ty =='MOD':
					if not flipped:
						root_sem = flip_parent(semantics,node,root_sem)
					root_sem = det(semantics,root_sem,True)
				#elif semantics[node.parents[0]].find_dep('n',semantics):
					#print 'merge these'
					#semantics[node.parents[0]].remove_dependent(semantics[node.parents[0]].find_dep('n',semantics).position,semantics)
					#node.add_dependent(semantics[node.parents[0]].find_dep('n',semantics).position,'???',semantics)
				else:
					#print 'different head'
					pass
	return root_sem


def mod(semantics,root_sem):
	## doing this before DET now - might want to fix that.
	for node in semantics:
		if node.ty == 'MOD' and node.pos =='-POSS':
			if len(node.parents)!=1:
				#print 'not one parent 250'
				pass
			else:
				if semantics[node.parents[0]].pos!='n' or not (semantics[node.parents[0]].find_dep('n',semantics)) or len(semantics[node.parents[0]].dependents)!=2:
					#print 'issues here'
					pass
					## maybe after det
			pass
		elif node.ty == 'MOD':
			pass #if 
			
	return root_sem

def adj(semantics,root_sem):
	for node in semantics:
		if node.pos == 'adj' and len(node.parents)==1:
			if semantics[node.parents[0]].pos == 'n' or semantics[node.parents[0]].pos == 'pro':
				root_sem = flip_parent(semantics,node,root_sem)
	return root_sem


def adv(semantics,root_sem):
	flipped_advs = []
	for node in semantics:
		if node.pos == 'adv' and len(node.parents) == 1:
			if (semantics[node.parents[0]].pos == 'v' or semantics[node.parents[0]].pos == 'part' or semantics[node.parents[0]].pos == 'adj' or semantics[node.parents[0]].pos == 'prep' or semantics[node.parents[0]].pos == 'aux') and not node.find_dep('v',semantics) and not node.find_dep('adv',semantics) and not node.find_dep('adj',semantics):
				root_sem = flip_parent(semantics,node,root_sem)
				#print 'flipping adv'
			elif  semantics[node.parents[0]].pos == 'pro:indef' or  semantics[node.parents[0]].pos == 'n':
				root_sem = flip_parent(semantics,node,root_sem)
				if node != root_sem:
					if semantics[node.parents[0]].ty == 'DET':
						root_sem = flip_parent(semantics,node,root_sem)
					#print 'done noun'
				#else: print 'root now'

			elif semantics[node.parents[0]].pos == 'adv':
				root_sem = flip_parent(semantics,node,root_sem)
				# they get them consistently wrong


				

			# needs to modify a verb or adjective - do MOD first!!!
			pass
	return root_sem
				

	
def wh(semantics,root_sem,punctuation,o):
	## really still confused as to what happens here
	##
	## first move to front v (and aux and neg)
	## then if not root - check with 
	
	wh = False
	for node in semantics:
		if node.pos.find('wh')!=-1:
			
			
			if len(node.parents)==1:
				if (semantics[node.parents[0]].pos == 'v' or semantics[node.parents[0]].pos == 'part' or semantics[node.parents[0]].pos == 'aux') and node.dependents == []:
					root_sem = flip_parent(semantics,node,root_sem)
					#print 'moved this'
					pass
				else:
					#print 'not moving this'
					pass
					## actually probably should move it out of N
					## and should also deal with wh as a COM
	
	if semantics[0].name.find('wh|')!=-1 and punctuation.name=='?':
		wh = semantics[0]
		if root_sem != wh:
			
			#print 'wh methinks'
			#print >> o,sentence
			#root_sem.print_tree(semantics,o)
			#print >> o,'\n'
			
			conj = False
			for node2 in semantics:
				if node2.name == 'conj:coo|and':
					print 'and too though'
					conj = True
			
			if root_sem.pos != 'aux':
				print 'root not aux'
			
			if not conj:
				print '@@@'
				if len(wh.parents)==1:
					parent = wh.parents[0]
					semantics[parent].remove_dependent(wh.position,semantics)
					print 'here::'
					for dep in wh.dependents:
						node.remove_dependent(dep.position,semantics)
						print 'removing wh dep'
						semantics[parent].add_dependent(dep.position,'??',semantics)
					
					wh.add_dependent(root_sem.position,'??',semantics)
					root_sem = wh
				#else: 
					#print >> o, 'parents are ',wh.parents
					#print >> o,sentence
					#root_sem.print_tree(semantics,o)
					#print >> o,'\n'
			
			
		#if not root_sem.position == 0:
			#for parent in semantics[0].parents:
				#semantics[parent].remove_dependent(0,semantics)
			#if len(semantics[0].dependents)>0:
				#print 'BOLLOX - GOT DEPENDENTS'
		
		
		#wh = True
	#else:
		#for node in semantics:
			#if node.name.find('wh|')!=-1 and punctuation.name=='?':
				#print 'not wh?'
	return root_sem


def com(semantics,root_sem):
	for node in semantics:
		if node.ty == 'COM':
			if node.pos.find('wh')!=-1:
				#print 'making root - :s'
				if len(node.parents)>1:
					#print 'COM has too many parents'
					pass
				elif  len(node.parents) ==1:
					semantics[node.parents[0]].remove_dependent(node.position,semantics)
					node.add_dependent(root_sem.position,'????',semantics)
					root_sem = node
			else:
				if len(node.parents)>1:
					#print 'COM has too many parents'
					pass
				elif  len(node.parents) ==1:
					if not semantics[node.parents[0]]==root_sem:
						semantics[node.parents[0]].remove_dependent(node.position,semantics)
						root_sem.add_dependent(node.position,'????',semantics)
	#normally attaches to root - unless is wh in which case move to front
	return root_sem


def voc(semantics,root_sem):
	for node in semantics:
		if node.ty == 'VOC':
			if len(node.parents)>1:
				#print 'COM has too many parents'
				pass
			elif  len(node.parents) ==1:
				if not semantics[node.parents[0]]==root_sem:
					semantics[node.parents[0]].remove_dependent(node.position,semantics)
					root_sem.add_dependent(node.position,'????',semantics)
					#print 'voc done'
	return root_sem


	


def quant(semantics,root_sem):
	for node in semantics:
		if node.ty == 'QUANT':
			if len(node.parents)>1:
				pass
			elif  len(node.parents)==1:
				if semantics[node.parents[0]].pos == 'n':
					if node.dependents == []:
						root_sem = flip_parent(semantics,node,root_sem)
					elif len(node.dependents)==1:
						if semantics[node.dependents[0].position].ty == 'JCT':
							father = node.parents[0]
							semantics[father].remove_dependent(node.position,semantics)
							if semantics[father].parents != []:
								for parent in semantics[father].parents:
									semantics[parent].remove_dependent(father,semantics)
									semantics[parent].add_dependent(node.position,'????',semantics)
							semantics[node.dependents[0].position].add_dependent(father,'????',semantics)
							if root_sem == semantics[father]:
								root_sem = node
							pass
						elif semantics[node.dependents[0].position].pos == 'qn':
							#print 'not expecting this'
							pass
					
					
					pass
				elif semantics[node.parents[0]].pos =='qn' and semantics[node.parents[0]].ty == 'JCT':
					if len(node.parents) !=1:
						#print 'JCT - QUANT error'
						pass
					else:
						root_sem = flip_parent(semantics,node,root_sem)
						#print 'flipped jct - quant'
						pass
				#else: print 'not n'
				
	return root_sem

def mod(semantics,root_sem):
	for node in semantics:
		if node.ty == 'MOD':
			if node.pos == '-POSS':
				if len(node.parents)==1:
					if semantics[node.parents[0]].pos == 'n':
						
						root_sem = exchange_parent(semantics,node,root_sem)
						#print '-poss sorted'
					#else: print '-poss error'
				pass
			else:
				if len(node.parents)==1:
					if (semantics[node.parents[0]].pos == 'n' or semantics[node.parents[0]].pos == 'pro:indef') and node.dependents == [] and not semantics[node.parents[0]].find_dep('-POSS',semantics):
						root_sem = flip_parent(semantics,node,root_sem)
					else:
						#print 'whadda hell'
						pass
						
			pass
	return root_sem


#############################################

### change cat gives each node a category of the type s|n, np|n, n
### the order of the dependents is IMPORTANT as is the definition of 
### which of AUX and V get to head SUBJ
def change_cat2(node,semantics,question):
	return
	#for node in semantics:
	if node.cat == 'null' and node.ty != 'PUNCT':
		if node.pos == 'aux':
			if question:
				node.cat = '{\sc s}$_{[y/n]}$'
			else:
				node.cat = '{\sc s}$_{[dcl]}$'
			pass
		elif node.pos=='v':
			if node.name.find('&'):
				node.cat = '{\sc s}$_{[dcl]}$'
			else:
				node.cat = '{\sc s}$_{[b]}$'
			pass
		elif node.pos =='part':
			node.cat = '{\sc s}$_{[dcl]}$'
			pass
		elif node.pos=='pro':
			if node.ty == 'SUBJ':
				node.cat = '{\sc np}$_{[SUBJ]}$'
			elif node.ty == 'OBJ':
				node.cat = '{\sc np}$_{[OBJ]}$'
			elif node.ty == 'PRED':
				node.cat = '{\sc np}$_{[PRED]}$'
			elif node.ty == 'POBJ':
				node.cat = '{\sc np}$_{[POBJ]}$'
			elif node.ty == 'ROOT':
				node.cat = '{\sc np}'
			elif node.ty == 'OBJ2':
				node.cat = '{\sc np}$_{[OBJ2]}$'
			elif node.ty == 'MOD':
				if len(node.dependents)!=1:
					print 'np_mod error'
				else:
					change_cat2(semantics[node.dependents[0].position],semantics,question)
					node.cat = semantics[node.dependents[0].position].cat
					if node.cat.find('NP')==-1:
						print 'np_mod error2'
			else: print 'none of these - is ',node.ty	
			pass
		elif node.pos=='pro:dem':
			node.cat = '{\sc np}$_{['+node.ty+']}$'
			pass
		elif node.pos=='pro:wh':
			node.cat = '{\sc s}$_{[wh]}$'
			node.wh_cat_shadow = '{\sc np}$_{['+node.ty+']}$'
			pass
		elif node.pos=='det':
			if len(node.dependents)!=1: print  'det error'
			else: node.cat = '{\sc np}$_{['+semantics[node.dependents[0].position].ty+']}$'
			pass
		elif node.pos=='qn':
			if len(node.dependents)!=1: print  'qn error'
			else: node.cat = '{\sc np}$_{['+semantics[node.dependents[0].position].ty+']}$'
			pass
		elif node.pos=='n':
			node.cat = '{\sc n}'
			pass
		elif node.pos=='adv':
			if len(node.dependents)!=1:
				print 'adv error'
			else:
				change_cat2(semantics[node.dependents[0].position],semantics,question)
				if semantics[node.dependents[0].position].cat != 'null':
					node.cat = semantics[node.dependents[0].position].cat
			pass
		elif node.pos=='adv:wh':
			node.cat = '{\sc s}$_{[wh]}$'
			node.wh_cat_shadow = '{\sc np}$_{['+node.ty+']}$'
			pass
		elif node.pos=='adv:loc':
			## not sure about these
			pass
		elif node.pos=='adj':
			## not sure about these
			if len(node.dependents)==1:
				change_cat2(semantics[node.dependents[0].position],semantics,question)
				if semantics[node.dependents[0].position].cat.find('NP')!=-1:
					node.cat = semantics[node.dependents[0].position].cat
				else:
					print 'adj has child but not np'
		elif node.pos == 'n:prop':
			node.cat = '{\sc np}$_{['+node.ty+']}$'
			pass
		elif node.pos == 'prep':
			node.cat = '{\sc pp}'
			# ????????
			pass
		elif node.pos == 'unk':
			pass
		elif node.pos == 'pro:poss:det':
			if len(node.dependents)!=1: print  'pro:poss:det error'
			else: node.cat = '{\sc np}$_{['+semantics[node.dependents[0].position].ty+']}$'
			pass
		elif node.pos == 'co':
			## throw away this semantics really
			pass
		elif node.pos == 'neg':
			if len(node.dependents)==1:
				change_cat2(semantics[node.dependents[0].position],semantics,question)
				node.cat = semantics[node.dependents[0].position].cat
			else: print 'NEGATION ERROR - NOT ONE CHILD'
			## this happens when it's added in silly places and when we have COM elements
			pass
		elif node.pos == 'adv:int':
			## this thing should always go outside an adj or adv - fix it
			pass
		elif node.pos == 'conj:coo':
			#ignoring these
			pass
		elif node.pos == 'pro:indef':
			node.cat = '{\sc np}$_{['+node.ty+']}$'
			pass
		elif node.pos == 'inf':
			node.cat = '{\sc s}$_{[to]}$'
			pass
		elif node.pos == 'pro:exist':
			node.cat = '{\sc np}$_{['+node.ty+']}$'
			pass
		elif node.pos == 'co:voc':
			# ignore this maybe
			pass
		elif node.pos == 'conj:subor':
			#if node.ty == 'CPZR':
			node.cat = '{\sc s}$_{[cpzr]}$'
			#else:
			#	print 'not CPZR!!!'
			pass
		elif node.pos == 'fil':
			## - hmm, eh - ignore this
			pass
		elif node.pos == 'det:num':
			if len(node.dependents)!=1: print  'det:num error'
			else: node.cat = '{\sc np}$_{['+semantics[node.dependents[0].position].ty+']}$'
			pass
		elif node.pos == 'on':
			#ignore for now - basically just pee+pee
			pass
		elif node.pos == 'post':
			# else, too - do special cases
			pass
		elif node.pos == 'pro:poss':
			if len(node.dependents)!=1: print  'pro:poss error'
			else: node.cat = '{\sc np}$_{['+semantics[node.dependents[0]].ty+']}$'
			pass
		elif node.pos == 'n:pt':
			pass
		elif node.pos == 'det:wh':
			pass
		elif node.pos == 'un#adj':
			pass
		elif node.pos == 'adv:tem':
			pass
		elif node.pos == 'adv:adj':
			pass
		elif node.pos == 'int':
			pass
		elif node.pos == 'pro:refl':
			pass
		elif node.pos == 'rel':
			pass
		elif node.pos == 'n:adj':
			pass
		elif node.pos == 'n:v':
			pass
		elif node.pos == 'n:let':
			pass
		elif node.pos == 'chi':
			pass
		elif node.pos == 'n:gerund':
			pass
		elif node.pos == 'un#v':
			pass
		elif node.pos == 'adj:n':
			pass
		elif node.pos == 'un#part':
			pass
		elif node.pos == 'wplay':
			pass
		elif node.name == '-POSS':
			if node.find_dep_type('SUBJ',semantics):
				node.cat = '{\sc np}$_{[SUBJ]}$'
			elif node.find_dep_type('OBJ',semantics):
				node.cat = '{\sc np}$_{[OBJ]}$'
			else: node.cat = 'NP' #print 'no cat for -poss' 
			pass
		else: print 'no actually, node is ',node.name,' ',node.pos,' ',node.ty


def digDownTy(semantics,node):
	return node.pos
	if node.ty in ["MOD","DET","NEG","QUANT"] and len(node.dependents)==1:
		return digDownTy(semantics,semantics[node.dependents[0].position])
	return node.ty

def getVerbs(vOut,semantics):
	for node in semantics:
		if node.pos in ["v","part"]:
			nodeKey = node.name+"( "
			tySet = []
			for a1 in node.dependents:
				a = semantics[a1.position]
				if a.ty!="PUNCT":
					ty = digDownTy(semantics,a)
					if ty == "": ty = "*"
					tySet.append(ty)
					if ty in ["JCT","CPZR"]: return
			#if not "SUBJ" in tySet:
			#tySet.append("SUBJ")
			tySet.sort()
			for ty in tySet:
				nodeKey = nodeKey+ty+" "
			nodeKey = nodeKey+")"
			if not vOut.has_key(nodeKey):
				vOut[nodeKey]=1
			else: vOut[nodeKey]+=1
			
