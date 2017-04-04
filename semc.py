###########################################
# This is where the SemComponent class    #
# lives. 								  #
###########################################
# we can lose a lot of the crap in this 
# class I think.
# 
# completely redesign. - need boolean conectives
# functions ?? predicates and constants.
# could even make all of them before hand from the 
# list of things seen.
#
# there should be a strong distinction between the 
# class that is used at parse time and that that is
# used to read in the dependencies.
###########################################
class Sem_Component:
	def __init__(self,name,ty,position,dependents):
		self.Name = name
				self.fineType = name.split('|')[0]
		self.Type = ty
		self.Dependents = []
		self.ShadowDeps = []
		self.terminal = False
		if dependents:
			for dep in dependents:
				if dep.find('*')!=-1:
					pos = int(dep.strip('*'))
					self.ShadowDeps
					self.Dependents.append(pos)
					shadow = True
				else:
					pos = int(dep)
					shadow = False
					self.Dependents.append(dep)
		self.Position = position
		## will also put span in here for cky
		self.under_deps = []
	def add_underdeps(self,semantic_components):
		for d in self.Dependents:
			self.under_deps.append(d)
			self.under_deps.extend(semantic_components[d].add_underdeps(semantic_components))
		return self.under_deps
	def check_arcs(self,semantic_lib,semantic_components):
		tp = 0
		tp2 = 0
		fp = 0
		fn = 0
		if semantic_lib[self.Position] is None:
			sem_comp = None
		else:
			sem_comp = semantic_components[semantic_lib[self.Position]]
		
		for d in self.Dependents:
			match = False
			if sem_comp is not None:
				for d2 in sem_comp.Dependents:
					if semantic_components[d2].Position == d.Position:
						#print 'true positive ',self.Position,' --> ', d.Position
						tp += 1
						match = True
			#else: print 'sem comp is none'
			if not match:
				#print 'no match ',self.Position,' --> ', d.Position
				fp +=1
			
			if semantic_lib[d.Position] is not None:
				r = d.check_arcs(semantic_lib,semantic_components)
				
				tp = tp + r[0]
				fp = fp + r[1]
			else:
				print 'Null for ',d.Position
				
		return (tp,fp)
			
			
			
	def check_arcs2(self,semantic_lib2,semantic_components):
		tp = 0
		fn = 0
		if semantic_lib2 is None:
			sem_comp = None
		else:
			if semantic_lib2.has_key(self.Position):
				sem_comp = semantic_lib2[self.Position]
			else: sem_comp = None
		for d in self.Dependents:
			match = False
			if sem_comp is not None:
				for d2 in sem_comp.Dependents:
					if semantic_components[d].Position == d2.Position:
						#print 'true positive2 ',self.Position,' --> ', d2.Position
						tp += 1
						match = True
			if not match:
				#print 'no match 2 ',self.Position,' --> ', semantic_components[d].Position
				fn +=1
			
			r = semantic_components[d].check_arcs2(semantic_lib2,semantic_components)
				
			tp = tp+r[0]
			fn = fn+r[1]
				
		return (tp,fn)
	
	def make_lib(self):
		lib = {}
		lib[self.Position] = self
		for d in self.Dependents:
			l2 = d.make_lib()
			for item in l2:
				lib[item] = l2[item]
		return lib
			
	def return_sem(self,semantic_components):
		self.sort_dep_by_name(semantic_components)
		sem = self.Name
		#if len(self.Dependents)>0:
			#sem = sem+'('
			#i = 1
			#for dep in self.Dependents:
				#sem = sem+semantic_components[dep].return_sem(semantic_components)
				#if i< len(self.Dependents):
					#sem = sem+','
				#i = i+1
			#sem = sem+')'
		return sem
	
	def return_span_sem(self,semantic_components,useable):
		if self.Position in useable:
			del useable[useable.index(self.Position)]
			sem_h = self.Name
			#print 'useable was ',useable
			#if self.Position in usesable:
				#del useable[useable.index(self.Position)]
			#print 'useable now ',useable
			after = []
			if len(self.Dependents)>0 and len(useable) > 0:
				sem = [sem_h+'(']
				i = 0
				no_reps = 1
				orders = tools.xcombinations(range(len(self.Dependents)),len(self.Dependents))
				sem = []
				for order in orders:
					sem1 = [(sem_h+'(',useable)]
					#print 'useable is ',useable
					#print 'order is ',order
					#o = set(order)
					#u = set(useable)
					for dep in order: #.union(u): #order and useable:
						if self.Dependents[dep] in useable:
							#print 'dep ',dep,' in order and useable'
							#useable2 = copy.deepcopy(useable)
							#del useable2[useable2.index(dep)]
							sem2 = []
							for s in sem1:
								useable2 = copy.deepcopy(s[1])
								s_n = s[0]
								#print 'looking into ',semantic_components[self.Dependents[dep]].Name
								after = semantic_components[self.Dependents[dep]].return_span_sem(semantic_components,useable2)
								if after:
									for a in after:
										s2 = copy.deepcopy(s_n)
										#print 's2 is ',s2
										if s2[len(s2)-1]!='(':
											s2 = s2+','
										s2 = s2+copy.deepcopy(a[0])
										#print 'appending ',a[0]
										sem2.append((copy.deepcopy(s2),a[1]))
								else:
									pass
							sem1 = copy.deepcopy(sem2)
							sem2 = []	
					sem.extend(copy.deepcopy(sem1))
				sem2 = []
				for s in sem:
					s2 = copy.deepcopy(s[0])
					s2 = s2+')'
					sem2.append((s2,s[1]))
				#print 'returning ',sem2
				return sem2
			else:
				#print 'returning ',(sem_h,useable)
				return [(sem_h,useable)]
		else:
			print 'Not in useable'
			return None
		
	def return_sem2(self,semantic_components):
		sem_h = self.Name
		after = []
		if len(self.Dependents)>0:
			sem = [sem_h+'(']
			i = 0
			no_reps = 1
			orders = tools.xcombinations(range(len(self.Dependents)),len(self.Dependents))
			sem = []
			for order in orders:
				sem1 = [sem_h+'(']
				for dep in order:
					sem2 = []
					for s in sem1:
						after = semantic_components[self.Dependents[dep]].return_sem2(semantic_components)
						for a in after:
							s2 = copy.deepcopy(s)
							if s2[len(s2)-1]!='(':
								s2 = s2+','
							s2 = s2+copy.deepcopy(a)
							sem2.append(copy.deepcopy(s2))
					sem1 = copy.deepcopy(sem2)
					sem2 = []	
				sem.extend(copy.deepcopy(sem1))
			sem2 = []
			for s in sem:
				s2 = copy.deepcopy(s)
				s2 = s2+')'
				sem2.append(s2)
			return sem2
		else:
			return [sem_h]

	# v|be&3S(pro:dem|that)(-POSS(n:prop|Eve)(n|seat))
	def return_sem3(self):
		sem = self.Name
		
		if sem.find('(') != -1:
			bits = sem.split('(')
			sem2 = bits[0]+'('
			if len(self.Dependents)>0:
				for dep in self.Dependents:
					sem2 = sem2+dep.return_sem3()
					sem2 = sem2+','
			for i in range(1,len(bits)):
				sem2 = sem2+bits[i]
			sem = sem2
			
		elif len(self.Dependents)>0:
			sem = sem+'('
			i=0
			for dep in self.Dependents:
				sem = sem+dep.return_sem3()
				if i<len(self.Dependents)-1:
					sem = sem+','
				i+=1
			sem = sem+')'
		
		return sem
	
	
	
	def print_name(self):
		print self.Name
		
	def generate_head(self, semantic_components):
		self.Head = self.Type
		#if len(self.Dependents)>0:
			#self.Head = self.Head+'('
			#i=1
			#for item in self.Dependents:
				#self.Head = self.Head+semantic_components[item].Type
				#if i!=len(self.Dependents): self.Head = self.Head+','
				#i=i+1
			#self.Head = self.Head+')'	
	def remove_dep(self,i):
		del_deps = []
		j = 0
		for d in self.Dependents:
			if d == i:
				#print 'removing ',i
				del_deps.append(j)
			j += 1
		del_deps.reverse()
		for d in del_deps:
			del self.Dependents[d]
			
	def sort_dependents(self,semantic_components):
		dependents = []
		if self.Dependents != [' ']:
			for item in self.Dependents:
				if int(item)<len(semantic_components):
					dependents.append((semantic_components[int(item)].Type, item))
			dependents.sort()
			self.Dependents = []
			for item in dependents:
				self.Dependents.append(int(item[1]))
	def sort_dep_by_name(self,semantic_components):
		## really need to do this before building the head rep innit
		dependents = []
		if self.Dependents != [' ']:
			for item in self.Dependents:
				if int(item)<len(semantic_components):
					dependents.append((semantic_components[int(item)].Name, item))
			dependents.sort()
			self.Dependents = []
			for item in dependents:
				self.Dependents.append(int(item[1]))
				
				
				
	

###########################################
