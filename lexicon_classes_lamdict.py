###########################################
# CLASSES USED TO CREATE THE LEXICON      #
###########################################

# there is some really unneccessary stuff
# in hear that needs cleaning out.
# LexicalisedSemantics anyone????

import copy
import random
from math import exp
from scipy.special import psi
from errorFunct import error


class Lambda_Rep:
	def __init__(self,type,name):
		self.type = type
		self.name = name
		self.dependents = []
		self.all_deps = []
		self.parents = []
		self.lambdas = {}
	def build_rep(self,sem_c,sem_comps,comps):
		for d in sem_c.Dependents:
			self.add_dep(comps[d])
			dep = comps[d].build_rep(sem_comps[d],sem_comps,comps)
			for d2 in dep.all_deps:
				if d2 not in self.all_deps:
					self.all_deps.append(d2)
		return self
	def add_dep(self,dep):
		self.dependents.append(dep)
		self.all_deps.append(dep)
		dep.make_parent(self)
	def make_parent(self,parent):
		self.parents.append(parent)
	def copy(self):
		s = copy.deepcopy(self)
		return s
	def print_self(self):	
		for l in self.lambdas:
			pass 
			print 'lambda_'+l.type,'.',
		print self.name+'(',
		for l in self.lambdas:
			if self.lambdas[l] is None:
				print l.type,',',
		for d in self.dependents:
			d.print_self()
			if self.dependents.index(d) != len(self.dependents)-1:
				print ',',
		print ')',
	def make_pairs(self):
		i = 0
		for d in self.all_deps:
			s = self.copy()
			if s.all_deps[i].make_var():
				print 'made pair for ',
				self.print_self()
				print ''
				s.print_self()
				print '   ',
				d.print_self()
				print '\n'
				s.make_pairs()
				d.make_pairs()
				i+=1
	def check_parent_branch(self,dep):
		#################################
		## this function checks whether #
		## a given dependent has a parent
		## on a different branch.
		## this only returns true if the#
		## node commands the piece of   #
		## l.f. itself.					#
		#################################
		for p in self.parents:
			if dep in p.dependents:
				return True
			for d in p.dependents:
				if d != self:
					if dep in d.all_deps:
						return True
			if p.check_parent_branch(dep):
				return True
		return False
		
	def make_var(self):
		print 'making var for ',
		self.print_self()
		print '' 
		other_branch = False
		for d in self.all_deps:
			if self.check_parent_branch(d):
				other_branch = True
		if not other_branch:
			for p in self.parents:
				p.make_lambda(self,None)
			self.parents = []
			return True
		else:
			return False
			
	def make_lambda(self,dep,separator):
		if dep in self.all_deps:
			# separator is the !node! that separates #
			# the dependent from the parent (often   #
			# None).								 #
			del_deps = []
			self.lambdas[dep] = separator
			
			##########################################
			# need to also delete lambdas shared with#
			# the child lambda list					 #
			##########################################
			for l in dep.lambdas:#.keys():
				if l in self.lambdas.has_key(l):
					del self.lambdas[l]	
			###########################################
			
			###########################################
			if dep in self.dependents:
				del self.dependents[self.dependents.index(dep)]
			del self.all_deps[self.all_deps.index(dep)]
			###########################################
			
			
			###########################################
			# Under_Deps are given the binary option  #
			# to go or stay							  #
			###########################################
			for d in self.all_deps:
				if d in dep.all_deps:
					#if d in self.dependents
					del_deps.append(d)
					
					#if 
					# but if it's in dependents (direct)
					# too then it will need a lambda term
					# _or_ it should stay here and the 
					# other thing should get a lambda
			##############################
			# should there be something  #
			# to deal with more complex  #
			# semantic possibilities?    #
			##############################		
			for p in self.parents:
				p.make_lambda(dep,self)
			# delete from all_deps here #
		
			for d in del_deps:
				del self.all_deps[self.all_deps.index(d)]
		#for d in self.dependents:
			#d.make_lambda(dep,
		
	# why does doing it like this help ? #
	# buddy, I'm not sure that it does.  #
	
	# have just recreated what I had before
	# need to support lx.f(x(a)) which I 
	# don't
	
	# do I really need to support this?
	# KIND OF IS SUPPORTED. SUBJ STILL 
	# THERE
	
	# NEED TO SPLIT SHARED ITEMS WHEN 
	# NECCESSARY. WOULD BE WELL NICE 
	# IF THIS WAS OPTIONAL TOO 
		
		
		
		
		
def make_lambda(sem_c,sem_comps,Parent,targ_rep,sem_store):
	comps = []
	for c in sem_comps:
		comps.append(Lambda_Rep(c.Type,c.Name))
	rep = comps[sem_comps.index(sem_c)].build_rep(sem_c,sem_comps,comps)
	rep.print_self()
	rep.make_pairs()
	
	

#class Lambda_Rep:
	#def __init__(self,sem_c,sem_comps,Parent,targ_rep,sem_store):
		#self.Head_Type = sem_c.Type
		#self.Head_Name = sem_c.Name
		#self.Position = sem_c.Position
		#self.Dependents = [] # these should probably be actual lambda reps themselves
		#self.UnderDeps = [] # these should also be actual lambda reps 
		#self.AllDeps = []
		#self.Lambdas = []
		#self.AllPairs = []
		#self.targets = {}#None
		#for d in sem_c.Dependents:
			#rep = Lambda_Rep(sem_comps[d],sem_comps,self,targ_rep,sem_store)
			#if rep == None:
				#print 'SELF LOOP1'
				#return None
				
			#elif rep.Position == self.Position:
				#print 'SELF LOOP2'
				#return None
			#if self.add_dep(rep) == None:
				#print 'SELF LOOP3'
				#return None
		#self.sort_Dependents()
		#self.set_parent_pos()
				
		#self.Parent = Parent
		#self.Lam_No = 0
		#self.sem_key = self.return_key(True)
		#self.make_pairs(sem_store)
		#sem_store.check(self)
	#def return_targets(self):
		#self.word_pos_start = self.Position
		#self.word_pos_end = self.Position + 1
		#self.bottom = True

		#s = self.copy()
		#for d in s.Dependents:
			#s.make_variable(d)

		##self.targets[(self.word_pos_start,self.word_pos_end)] = (s,self.copy())

		#for d in self.Dependents:
			#d.rep.return_targets()
			#self.targets.update(d.rep.targets)
		#self.targets[(self.word_pos_start,self.word_pos_end)] = (s,self.copy())
		#return self.targets.keys()
	
	#def return_templates(self):
		#t = self.copy()
		#t.Head_Name = ''
		#temps = []
		#for d in t.Dependents:
			#if d.rep:
				#temps.extend(d.rep.return_templates())
				#t.make_variable(d)
		#temps.append((t.return_key(False),self.return_key(False)))
		#return temps	
	
	#def add_dep(self,rep):#sem_h,sem_comps):
		#dep = Dependent(rep.Head_Type,rep,None)
		#self.Dependents.append(dep)
		#self.AllDeps.append(dep)
		#for d in dep.rep.AllDeps:
			#dep_below = Dependent(d.Dep_Type,d.rep,dep)

			#if dep_below.rep.Position == self.Position:
				#print 'SELF LOOP4'
				#return None
							
			#dep_below.Parent = dep				
			#self.UnderDeps.append(dep_below)
			#self.AllDeps.append(dep_below)
			
			
		
		##self.sort_Dependents()
		##return dep
		#return True
	#def set_parent_pos(self):
		#for d in self.AllDeps:
			#if d.Parent:
				#d.Parent_Pos = self.Dependents.index(d.Parent)
				##d.Parent = None
			#else:
				##print 'no parent for ',d.rep.return_key(True)
				#d.Parent_Pos = None
	##def clone(self):
		##this should create a clone as deep as possible
		##pass
	#def sort_Dependents(self):
		#d = []
		#i = 0
		#for dep in self.Dependents:
			##should maybe do this so that it can define between (e.g) NPs
			#d.append((dep.Dep_Type,i))
			#i += 1
		#d.sort()
		#d2 = []
		#for dep in d:
			#d2.append(self.Dependents[dep[1]])
		#self.Dependents = d2
		
	#def copy(self):
		#rep = copy.deepcopy(self)
		#return rep
	#def return_dep(self,rep):
		#for d in self.AllDeps:
			#if d.rep == rep:
				#return d
		#print 'not found d'
		#print 'target is '
		#rep.print_self(True)
		#print 'ds are '
		#for d in self.AllDeps:
			#d.print_self()
			#print ''
		#return None
	#def combine(self,rep,Join_Pos):
		#comb = False
		#r_l = []
		#for l in self.Lambdas:
			#r_l.append(l.Type)	

		#r_l.reverse()
		#if rep.Head_Type in r_l:
			#i = len(self.Lambdas) -1 - r_l.index(rep.Head_Type)
			#l = self.Lambdas[i]
			#if not l.Type == rep.Head_Type:
				#print 'MAJOR ERROR COMBINE'
			
			#if l.Type == rep.Head_Type:
				#if l.Direct_Or_Child == True:
					#self.Dependents[l.Pos].rep = rep
					##self.Dependents[l.Pos].Parent = 
					#self.AllDeps.append(self.Dependents[l.Pos])
					##self.AllDeps.extend(rep.AllDeps)
					##self.UnderDeps.extend(rep.AllDeps)
					#for d in rep.AllDeps:
							#d2 = copy.deepcopy(d)
							#d2.Parent_Pos = l.Pos
							#self.AllDeps.append(d2)
							#self.UnderDeps.append(d2)
					#comb = True
					#if l in self.Lambdas:
						#del self.Lambdas[self.Lambdas.index(l)]
					#else:
						#print '\n\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nMAJOR ISSUE WITH COMBINE1\n\n\n\n'
					
					#if rep.Lambdas != []:
						#Lam = copy.deepcopy(rep.Lambdas)
						#Lam.reverse()
						#for L in Lam:
							#L.Pos = l.Pos
							#self.Lam_No += 1
							#L.Number = self.Lam_No
							#L.Direct_Or_Child = False
							#self.Lambdas.append(L)


				#elif l.Direct_Or_Child == False:
					#if self.Dependents[l.Pos].rep:
						#comb = self.Dependents[l.Pos].rep.combine(rep,Join_Pos)
						##self.Dependents[l.Pos]
						#self.AllDeps.append(self.Dependents[l.Pos])
						#self.UnderDeps.append(self.Dependents[l.Pos])
						#for d in rep.AllDeps:
							#d2 = copy.deepcopy(d)
							#d2.Parent_Pos = l.Pos
							#self.AllDeps.append(d2)
							#self.UnderDeps.append(d2)
						
						#if l in self.Lambdas:
							#del self.Lambdas[self.Lambdas.index(l)]
						#else:
							#print '\n\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nMAJOR ISSUE WITH COMBINE1\n\n\n\n'
					
						#if rep.Lambdas != []:
							#Lam = copy.deepcopy(rep.Lambdas)
							#Lam.reverse()
							#for L in Lam:
								#L.Pos = l.Pos
								#self.Lam_No += 1
								#L.Number = self.Lam_No
								#L.Direct_Or_Child = False
								#self.Lambdas.append(L)					
					
					#else: 
						#print 'empty position'
		#else:
			##print 'not got lambda - you nutta'
			##self.print_self(True)
			##print ''
			##print rep.Head_Type
			#pass
		
		#if comb and rep.word_pos_start != None and self.word_pos_start != None and rep.word_pos_end != None and self.word_pos_end != None and Join_Pos:
			#if self.word_pos_start < rep.word_pos_start:
				#if not self.word_pos_end == rep.word_pos_start:
					#print 'comb error 499'
					#return None
					##abort()
				#else:
					#self.word_pos_end = rep.word_pos_end
				#pass
			#elif self.word_pos_start > rep.word_pos_start:
				#if not rep.word_pos_end == self.word_pos_start:
					#print 'comb error 499'
					##print 
					#print rep.word_pos_end,'    ',self.word_pos_start
					#return None
					##abort()
				#else:
					#self.word_pos_start = rep.word_pos_start
				#pass
			#else:
				#print 'comb error 502'
				#abort()
		#elif comb and Join_Pos:
			#print 'not all positions full ',rep.word_pos_start,self.word_pos_start,rep.word_pos_end,self.word_pos_end
		#return comb
		
		#pass
	
	#def make_pairs(self,sem_store):
		#i = 0
		#self.AllPairs = []
		##print 'making pairs for ',self.sem_key
		#for d in self.AllDeps:
		##	print 'making rep for ',d.rep.sem_key
			#s = self.copy()
			#(s1,s2) = s.make_variable(s.AllDeps[i])
			#if s1 and s2:
				#sem_store.check(s2)
				#self.AllPairs.append((s1.sem_key,s2.sem_key))
				##print 'added 
				##if not sem_store.check(s1):
				##sem_store.check(s1)
				#s = s1.copy()
				#s.make_pairs(sem_store)
				#sem_store.check(s)

			#i+=1
		
	#def make_variable(self,dep):
		#rem_pos = None
		###################################
		### when substitution rules are  ##
		### used, this function will have##
		### to be modified				##
		###################################
		### THIS IS AN OLD NOTE:         ##
		###	what are substitution rules??#
		###################################
		
		#if not dep in self.AllDeps:
			#print 'In, ',self.print_self(True)
			#print 'Not got dep ',dep.print_self()
			#print '\n'
			
		#elif dep.rep == None:
			#print 'rep ,',dep.print_self()
			#print 'Already gone buddy, from head'
			#print self.Head_Type,self.Head_Name
			
		#else:
			#target = dep.rep
			#if dep in self.Dependents:
				#########################################
				## identify the lambda terms that point #
				## to lower level terms and delete them #
				## from here							   #
				#########################################
				
				#del_lambdas_i = []
				#position = self.Dependents.index(dep)
				#for l in self.Lambdas:
					## check if they go to something parented by this
					#if l.Pos == position and l.Direct_Or_Child == False:
						##print 'removing lambda ',l.print_self()
						#del_lambdas_i.append(self.Lambdas.index(l))
						#del_lambdas = l
				
				#del_lambdas_i.reverse()
				#for l in del_lambdas_i:
					#del self.Lambdas[l]
				
				#########################################


				#l = Lambda_Term(dep.Dep_Type,self.Dependents.index(dep),True,self.Lam_No)
				#self.Lam_No += 1	
				#self.Lambdas.append(l)
				
				#dep.make_var()
				
				#i = self.Dependents.index(dep)
				#self.Dependents[i] = dep
				
				
				
				##############################################
				### identify the lower level dependents and ##
				### take them out of AllDeps 			   ##
				##############################################
				
				#del_deps = []
				#del_deps_u = []
				#i = 0
				#for d in self.AllDeps:
					#if d.Parent_Pos == self.Dependents.index(dep):
						#del_deps.append(i)
					#i+=1
					
				#del_deps.reverse()
				#for d in del_deps:
					#del self.AllDeps[d]
					
				#i = 0	
				#for d in self.AllDeps:
					#if d.Parent_Pos == self.Dependents.index(dep):
						#del_deps.append(i)
					#i+=1	
					
				#del_deps_u = []
				#i = 0
				#for d in self.UnderDeps:
					#if d.Parent_Pos == self.Dependents.index(dep):
						#del_deps_u.append(i)
					#i+=1
				#del_deps_u.reverse()
				#for d in del_deps_u:
					#del self.UnderDeps[d]
					

				##############################################						
				## AllDeps is used for choosing lambda terms #
				## so delete the dependent from this 		# 
				##############################################						
								
				#del self.AllDeps[self.AllDeps.index(dep)]
			#elif dep in self.UnderDeps:			
				### Need to delete some Lambdas from here    ##
				### This is done by passing back which number #
				### in the order of identical type ls that it #
				### should be 								 #
				#if dep.rep.Lambdas != []:
					#i = 0
					#lambda_del = []
					#lambda_temp = copy.copy(dep.rep.Lambdas)
					#lambda_temp.reverse()
					#for l in lambda_temp: #dep.rep.Lambdas:
						#if l.Type!=self.Lambdas[len(self.Lambdas)-1-i].Type:
							#print 'LAMBDA MISMATCH'
							#print 'i is ',i
							#print 'self type is ',self.Lambdas[len(self.Lambdas)-1-i].Type
							#print 'l.type is ',l.Type
							#print 'all are'
							#for lam in self.Lambdas:
								#print lam.Type
							#return (None,None)
						#else:
							##print 'goinna delete ',len(self.Lambdas)-1-i
							#lambda_del.append(len(self.Lambdas)-1-i)
						#i+=1	
					#for l in lambda_del:
						#del self.Lambdas[l]

				#l = Lambda_Term(dep.Dep_Type,dep.Parent_Pos,False,self.Lam_No)
				#self.Lam_No += 1
				#self.Lambdas.append(l)
				#Parent = self.Dependents[dep.Parent_Pos].rep
				#################################################
				### this is the dependent as it belongs to the ##
				### child/parent        						  ##
				#################################################						
				#d_new = Parent.return_dep(dep.rep)	
				#if d_new:
					#self.Dependents[dep.Parent_Pos].rep.make_variable(d_new)
				#else:
					#print 'returning none for ',dep.rep.Head_Name
					#print 'parent is ',
					#self.Dependents[dep.Parent_Pos].rep.print_self(True)
					#return None
				
				#del self.UnderDeps[self.UnderDeps.index(dep)]
				#del self.AllDeps[self.AllDeps.index(dep)]
				
				### get rid of all dependents fathered by the new variable ##
				### but also need to get rid of all lambda terms ##
				
				#rid_of_deps = []
				#for d in target.AllDeps:
					#rid_of_deps.append(d.rep)

				#del_deps = []
				#del_all_deps = []
				#i = 0
				#for d in self.UnderDeps:
					#if d.rep in rid_of_deps and d.Parent_Pos == dep.Parent_Pos:
						#del rid_of_deps[rid_of_deps.index(d.rep)]
						#del_deps.append(self.UnderDeps.index(d))
						#del_all_deps.append(self.AllDeps.index(d))
					#i+=1

				#if len(rid_of_deps) != 0:
					#print 'Error for rid of deps. Has'
					#for d in rid_of_deps:
						#d.print_self()
						#print '' 
					#print '\n'	
				#del_deps.reverse()
				#for i in del_deps:
					#del self.UnderDeps[i]
					
				#del_all_deps.sort()
				#del_all_deps.reverse()
				#del i
				#for i in del_all_deps:
					#del self.AllDeps[i]
			#else: 
				
				#print 'IN NEITHER - WOAAAH !!!!!!!!'
				#print 'dep is'
				#dep.print_self()
				#print 'in rep'
				#self.print_self(True)
				
			#self.sem_key = self.return_key(True)
			
			#target.sem_key = target.return_key(True)
			
			#return (self,target)
	
	#def set_unk(self):
		#self.Head_Name = 'unk'
		#for d in self.Dependents:
			#d.set_unk()
	#def return_span_dict(self,span):
		#for i in range(2,span+1): ## length of span
			#for j in range(span-i+1): ## start of span
				#for k in range(1,i): ## partition of span
					#if self.targets.has_key((j,j+k)) and self.targets.has_key((j+k,j+i)):
						
						#l = self.targets[(j,j+k)][0].copy()
						#r = self.targets[(j+k,j+i)][0].copy()
						#comb1 = l.combine(r,True)
						#if comb1:
							#self.targets[(j,j+i)] = (l,self.targets[(j,j+k)][1].copy())
							
						#l = self.targets[(j,j+k)][0].copy()
						#r = self.targets[(j+k,j+i)][0].copy()
						#comb2 = r.combine(l,True)
						#if comb2:
							#self.targets[(j,j+i)] = (r,self.targets[(j+k,j+i)][1].copy())
						
		##print 'matrix has  ',self.targets.keys()
		#return self.targets
	#def print_self(self,Top):
		
		#if Top:
			#l = self.Lambdas
			#l.reverse()
			#for item in l:
				#item.print_self()
			#l.reverse()
			#if len(self.Lambdas)>0:
				#print '.',
				
		#print self.Head_Name,
		#print '::[',self.Head_Type,']',
		#if self.Dependents != []:
			#print '(',
			#i = 1
			#for d in self.Dependents:
				#d.print_self()
				#if i<len(self.Dependents):
					#print ',',
				#i += 1
			#print ')',
			
	#def return_key(self,Top):
		#key = ''
		#if Top:
			#l = self.Lambdas
			#l.reverse()
			#for item in l:
				#key = key+item.return_key()
			#if len(self.Lambdas)>0:
				#key = key+'.'
			#l.reverse()
		#key = key+self.Head_Name
		#key = key+'::['+self.Head_Type+']'
		#if self.Dependents != []:
			#key = key+'('
			#i = 1
			#for d in self.Dependents:
				#key = key+d.return_key()
				#if i<len(self.Dependents):
					#key = key+','
				#i += 1
			#key = key+')'
		#return key
	#def all_marks(self):
		#all_marks = 1
		#for d in self.Dependents:
			#if d.rep:
				#all_marks += 1
				## one for the link
				#all_marks = all_marks + d.rep.all_marks()
		#return all_marks
	#def return_components(self):
		#components = []
		#if self.Dependents != []:	
			#for d in self.Dependents:
				#if d.rep:
					#(r,t) = self.make_variable(d)
					#components.extend(t.return_components())
						
		#components.append((self.return_key(False),self))
		#return components
##	
#
class Dependent:
	def __init__(self,Dep_Type,rep,Parent):
		self.Dep_Type = Dep_Type
		self.Parent = Parent
		self.Parent_Pos = None
		if rep: self.rep = rep # this should actually be a full lambda rep
		else: self.rep = None
		# maybe we should be able to set the number here
	def make_var(self):
		self.rep = None
	def set_unk(self):
		if self.rep:
			self.rep.set_unk()
	def print_self(self):
		#print self.Dep_Type,
		if self.rep is None:
			print self.Dep_Type,
		else:
			self.rep.print_self(False)

	def return_key(self):
		if self.rep is None:
			key = self.Dep_Type
		else:
			key = self.rep.return_key(False)
		return key
					
		## need to allow it to say which lambda terms are its children
	#this won't be any good for lower links
	def return_reqd_type(self,Parent):
		reqd_type = self.Dep_Type
		if self.rep.Lambdas != []:
			proceed = True
			reqd_type = reqd_type+'-'
			i = 0
			
			for l in self.rep.Lambdas:
				p = Parent.Lambdas[len(Parent.Lambdas)-1-i].Pos
				if not p == self.Parent_Pos and not (self in Parent.Dependents and p == Parent.Dependents.index(self)):
					proceed = False
					#pass
					#proceed = True
				#elif self in Parent.Dependents and p == Parent.Dependents.index(self):
						#pass #proceed = True
				#else:
					#proceed = False		
				i+=1		
			
			if proceed:
				i = 0	
				for l in self.rep.Lambdas:
					reqd_type = reqd_type+l.Type
					if i < len(self.rep.Lambdas)-1:
						reqd_type = reqd_type+'_'
					i+=1 
			else:
				reqd_type= None
		return reqd_type
		
class Lambda_Term:
	def __init__(self,Lambda_Type,Pos,Direct,Number):
		self.Type = Lambda_Type
		#self.UnderLambda = UnderLambda
		self.Direct_Or_Child = Direct
		#self.Parent = ?? # this should say which dependent is the parent
		self.Children = []
		## Number tells us where the thing is that this should bind to - will just be a list index
		self.Pos = Pos
		self.Number = Number
		## children will say which lambda terms should be controlled by the current one
		## how should this all be stored in the lexicon though??
		
	def add_children(self):
		pass
	
	def print_self(self):
		print '$\\lambda$',self.Pos,'_{',self.Type,'}',
	def return_key(self):
		return '$lambda$'+str(self.Pos)+'_{'+self.Type+'}'	


#
#
class Semantic_Model:
	def __init__(self):
		self.semantic_components = {}
		self.lexicalised_semantics = {}
		self.alpha_c_top = 1000
	def check_sem(self,rep):
		if not self.lexicalised_semantics.has_key(rep.return_key(True)):
			self.lexicalised_semantics[rep.return_key(True)] = LexicalisedSemantics(rep.copy(),self)
			#print 'added ',rep.return_key(True)
	def check_atom(self,a):
		if not self.semantic_components.has_key(a[0]):
			self.semantic_components[a[0]] = Semantic_Atom(a[1])
			#self.lexicalised_semantics[a[1].return_key(True)]
		#self.semantic_components[a[0]].increment_alpha()
	def get_prob(self,sem):
		#print 'getting prob for ',sem
		if sem:
			prob = self.lexicalised_semantics[sem].return_prob(self)
		else:
			prob = float(1)
		return prob
		#alpha
	def increment_alpha(self,sem,alpha):
		self.lexicalised_semantics[sem].increment_alpha(alpha,self)
#
#
class Semantic_Atom:
	def __init__(self,rep):
		self.rep = rep.copy()
		self.key = self.rep.return_key(True)	
		self.targets = {}
		self.alpha = 0
		self.alpha_top = float(1)
	def add_target(self,key):
		self.targets[key] = key#pass
	def increment_alpha(self,alpha):
		self.alpha = self.alpha + alpha
	def return_alpha_max(self,sem_model):
		alpha_max = 0
		for t in self.targets:
			if sem_model.lexicalised_semantics[t].alpha > alpha_max:
				alpha_max = sem_model.lexicalised_semantics[t].alpha
		return alpha_max
		


class LexicalisedSemantics:
	def __init__(self,rep,sem_model):
		self.rep = rep.copy()
		self.components = rep.return_components()
		#for c in self.components:
			#if not sem_model.semantic_components.has_key(c[0]):
			#	sem_model.check_sem(c[0])
			#sem_model.semantic_components[c[0]].add_target(self.rep.return_key(True))
		self.alpha = 0  
		self.atomic_types = [ 'PP' , 'VP_[to]' , 'NP_[SUBJ]' , 'S_[y/n]' , 'NP_[OBJ]' , 'NP_[POBJ]' , 'NP_[PRED]' , 'N' , 'NP' , 'NP_[OBJ2]' , 'VP_[perf]' , 'S_[dcl]' , 'VP_[ing]' , 'S_[emb]' , 'VP_[b]' , 'S_[wh]' ]
		#if len(self.components)==1:
			#self.alpha = 1.0
		#print '\n'
		#self.rep.print_self(True)
		#print ' has components ',
		#print self.components,'\n'		
	def return_prob(self,sem_model):
		prob = float(1)
		prob_seen = float(1)
		prob_unk = float(1)
	
		for c in self.components:
			p_seen_c = self.alpha/(sem_model.semantic_components[c[0]].alpha+sem_model.semantic_components[c[0]].alpha_top)
			p_new = sem_model.semantic_components[c[0]].alpha_top/(sem_model.semantic_components[c[0]].alpha+sem_model.semantic_components[c[0]].alpha_top)
			
			prob_seen = prob_seen*p_seen_c
			prob_unk = prob_unk*p_new
		
		prior = self.get_lex_prior()
		prob = prob_seen + prob_unk*prior
		return prob
		

	def get_lex_prior(self):
		prob = float(1)
		if len(self.components)>1:
			prob = prob*pow(float(1)/33,2*(len(self.components)-1))
		prior = prob*pow(0.5,len(self.components))
		return prior
		
	def get_prior_given_syn(self):

		prior = 1.0
		for c in self.components:
			#print 'c is ',c
			s_temp = c[0].split('::')[0]
			if s_temp.find('|')!=-1:
				s_name = s_temp.split('|')[1]
			elif s_temp == '-POSS':
				s_name = 'POSS'
			else:
				print 'comp error'
				error('comp error')
			#prior = prior/len(self.atomic_types)
			prior = prior*pow(1.0/48,len(s_name))

		prior = prior/pow(len(self.atomic_types),len(self.components)-1)
		
		if len(self.components)<1:
			print 'no components line 1084'
			error('no components line 1084')
		return prior
		
	def increment_alpha(self,alpha,sem_model):
		self.alpha = self.alpha + alpha
		for c in self.components:
			sem_model.semantic_components[c[0]].increment_alpha(alpha)
	def remove_trace(self,lexicon):
		for c in self.components:
			if lexicon.sem_model.semantic_components.has_key(c[0]) and lexicon.sem_model.semantic_components[c[0]].targets.has_key(self.rep.return_key(True)):
				del lexicon.sem_model.semantic_components[c[0]].targets[self.rep.return_key(True)]
		if lexicon.semantics.has_key(self.rep.return_key(True)):
			for l in lexicon.semantics[self.rep.return_key(True)]:
				lexicon.delete_lex_item[l]
	
#


class Lexicon:
	def __init__(self):
		self.lex = {}
		self.sem_model = Semantic_Model()
		
		self.words = {}
		self.semantics = {}
		self.syntax = {}
		
		
		self.syn_sem = {}
		#self.Sem_Atoms = Sem_Bag() ## for p(sem_c|sem_bag)
		#self.semlex = LexicalisedSemSet() ## for p(sem_lex|sem_c)
		
		self.alpha_top = float(0.01)
		
	def delete_lex_item(self,item):
		
		#print 'deleting ', item
		w = item[0]
		sem = item[1]
		syn = item[2]
		if self.words.has_key(w):
			del self.words[w][self.words[w].index(item)]
			#print 'word is '
			#print  self.words[w]
			#print 'item is ',item
			#del self.words[w][item]
		if self.syntax.has_key(syn):	
			if item in self.syntax[syn]:
				del self.syntax[syn][self.syntax[syn].index(item)]
		if self.semantics.has_key(sem):
			if item in self.semantics[sem]:
				del self.semantics[sem][self.semantics[sem].index(item)]
		if self.syn_sem.has_key((syn,sem)):
			if item in self.syn_sem[(syn,sem)]:
				del self.syn_sem[(syn,sem)][self.syn_sem[(syn,sem)].index(item)]
		
		del self.lex[item]
		
		pass
	def delete_sem_item(self,item):
		#print 'should delete ',item
		if self.sem_model.lexicalised_semantics.has_key(item):
			self.sem_model.lexicalised_semantics[item].remove_trace(self)
			del self.sem_model.lexicalised_semantics[item]
		pass	
	def add_copy_lex(self,l_i):
		self.lex[l_i.key] = copy.deepcopy(l_i)
		key = l_i.key
		word = l_i.word
		sem_key = l_i.sem_key
		syn = l_i.syn
		if not self.words.has_key(word):
			self.words[word] = [key]
		else: self.words[word].append(key)
		
		if not self.semantics.has_key(sem_key):
			self.semantics[sem_key] = [key]
		else: self.semantics[sem_key].append(key)
		
		if not self.syntax.has_key(syn):
			self.syntax[syn] = [key]
		else: self.syntax[syn].append(key)
		
		if not self.syn_sem.has_key((syn,sem_key)):
			self.syn_sem[(syn,sem_key)] = [key]
		else: self.syn_sem[(syn,sem_key)].append(key)
	def add_copy_sem(self,sem):
		self.sem_model.lexicalised_semantics[sem.rep.return_key(True)]= copy.deepcopy(sem)


	def check_sem_prob(self,s):
		sem = self.sem_model.lexicalised_semantics[s]
		alpha_max = 1
		for c in sem.components:
#			print 'has component ',c[0]
			alpha_max = alpha_max*self.sem_model.semantic_components[c[0]].return_alpha_max(self.sem_model)
		if sem.alpha > alpha_max/10000:
	#		print 'returning true'
			return True
		else:
		#	print 'alpha is ',sem.alpha
			#print 'alpha max is ',alpha_max
			return False
			
	def tidy(self):
		
		lex_del = []
		sem_keep = []
		syn_sem_keep = []
		for s in self.syn_sem:
			alpha_max = 0
			for l in self.syn_sem[s]:
				if self.lex[l].alpha > alpha_max:
					alpha_max = self.lex[l].alpha

			for l in self.syn_sem[s]:
				if self.lex[l].alpha > alpha_max/50:
					if self.check_sem_prob(l[1]):
						if not l[1] in sem_keep:
							sem_keep.append(l[1])
						if not s in syn_sem_keep:
							syn_sem_keep.append(s)
					else:
						lex_del.append(l)
				else:
					lex_del.append(l)
				

		for l in lex_del:
			del self.lex[l]
			w = self.words[l[0]]
			del w[w.index(l)]
			sem = self.semantics[l[1]]
			del sem[sem.index(l)]
			syn = self.syntax[l[2]]
			del syn[syn.index(l)]
			syn_sem = self.syn_sem[(l[2],l[1])]
			del syn_sem[syn_sem.index(l)]

		sem_del = []
		for s in self.semantics:
			if s not in sem_keep:
				self.sem_model.lexicalised_semantics[s].remove_trace(lexicon)
		
				del self.sem_model.lexicalised_semantics[s]
				sem_del.append(s)
		for s in sem_del:
			del self.semantics[s]
		syn_sem_del = []
		for s in self.syn_sem:
			if s not in syn_sem_keep:
				syn_sem_del.append(s)
		for s in syn_sem_del:
			del self.syn_sem[s]
			
		return self	

	def has(self,word,sem_key,syn):
		key = (word,sem_key,syn)
		if self.lex.has_key(key):
			return True
		else: return False
		
	def add(self,word,sem_key,syn):
		key = (word,sem_key,syn)
		self.lex[key] = lexical_item(word,sem_key,syn)
		if not self.words.has_key(word):
			self.words[word] = [key]
		else: self.words[word].append(key)
		
		if not self.semantics.has_key(sem_key):
			self.semantics[sem_key] = [key]
		else: self.semantics[sem_key].append(key)
		
		if not self.syntax.has_key(syn):
			self.syntax[syn] = [key]
		else: self.syntax[syn].append(key)
		
		if not self.syn_sem.has_key((syn,sem_key)):
			self.syn_sem[(syn,sem_key)] = [key]
		else: self.syn_sem[(syn,sem_key)].append(key)
		
		return  self.lex[key]
	
	def increment_count(self,key):
		self.lex[key].increment_count(self)
	def total_alpha_syn(self,syn_key):
		alpha_tot = 0
		for key in self.syntax[syn_key]:
			alpha_tot = alpha_tot + self.lex[key].alpha
		return alpha_tot
		
	def total_alpha_sem(self,sem_key):
		alpha_tot = 0
		for key in self.semantics[sem_key]:
			alpha_tot = alpha_tot + self.lex[key].alpha
		return alpha_tot
		
	def total_alpha_syn_sem(self,syn_sem_key):
		alpha_tot = 0
		if self.syn_sem.has_key(syn_sem_key):
			for key in self.syn_sem[syn_sem_key]:
				alpha_tot = alpha_tot + self.lex[key].alpha
		return alpha_tot

	def total_alpha_word(self,word):

		alpha_tot = 0
		for key in self.words[word]:
			alpha_tot = alpha_tot + self.lex[key].alpha
		return alpha_tot

	#def get_sem_prior(self,sem):
		#sem_rep = self.sem_model.lexicalised_semantics[sem]
		#prior = 1.0
		#for c in sem_rep.components:
		#	s_name = c[0].split('::')[0].split('|')[1]
		#	prior = prior/len(self.atomic_types)
		#	prior = prior*pow(1.0/48,len(s_name))
		#return prior
	
	def p_sem_given_syn(self,syn,sem):
		#return None
		if sem:
			alpha_syn_sem = self.total_alpha_syn_sem((syn,sem))
			Prior = self.sem_model.lexicalised_semantics[sem].get_prior_given_syn()
			#Prior = self.get_sem_prior(sem)
		else:
			# only used when sem is not known in prediction
			alpha_syn_sem = 0
			Prior = float(1)
		
		alpha_syn = self.total_alpha_syn(syn)
		if alpha_syn_sem != 0:
			P_seen = exp(psi(alpha_syn_sem))/exp(psi(alpha_syn+self.alpha_top))
		else:
			P_seen = 0
		P_new =exp(psi(self.alpha_top) - psi(alpha_syn+self.alpha_top))
		
		#Prior = self.sem_model.lexicalised_semantics[sem].get_prior_given_syn()
			

		P = P_seen + P_new*Prior
		return P
	
	
	def p_word_given_sem_syn(self,word,sem,syn):
		if sem:
			alpha_syn_sem = self.total_alpha_syn_sem((syn,sem))
			
			key = (word,sem,syn)
			
			alpha_l = self.lex[key].alpha

			if alpha_l > 0:
				P_seen = exp(psi(alpha_l))/exp(psi(alpha_syn_sem+self.alpha_top))
			else:
				P_seen = 0

			P_new = exp(psi(self.alpha_top) - psi(alpha_syn_sem+self.alpha_top))
			
			Prior = self.lex[key].set_word_prior()
			
			
			P = P_seen + P_new*Prior
		else:
			alpha_syn = self.total_alpha_syn(syn)
			P_new = exp(psi(self.alpha_top) - psi(alpha_syn+self.alpha_top))
			Prior = self.set_word_prior(word)
			
			P = P_new*Prior

		return P
	def set_word_prior(self,word):
		no_char = len(word) - word.count(' ')
		w_prior = pow((float(1)/24),no_char)
		return w_prior
	def update_alpha(self,key,a):
		self.lex[key].update_alpha(a)
	##
	##
	def get_words_from_sem_syn(self,sem,syn,lexicon):
		
		words = []
		if self.syn_sem.has_key((syn,sem)):
			for l in self.syn_sem[(syn,sem)]:
				word = l[0]
				prob_sem = lexicon.p_sem_given_syn(syn,sem)
				prob = lexicon.p_word_given_sem_syn(word,sem,syn)
				words.append((prob,word))
			
			words.sort()
			words.reverse()
			
		else:
			return None
		
		# should add something more like a probability threshold here
		
		return words[0]
		
	def find_word(self,word,lexicon):
		final_set = []
		if self.words.has_key(word):
			items = self.words[word]
			if len(items) > 0:
				set = []
				set2 = []
				for item in items:
					set2.append((self.lex[item].alpha,item))

				if set2 != []:
					alpha_max = set2[0][0]
					alpha_min = set2[len(set2)-1][0]
					set2.sort()
					set2.reverse()
					
					for item in set2:
						if item[0] > alpha_max/50 and len(final_set) < 20:
							final_set.append(item)
				
		elif word.find(' ')==-1:
			cats = []
			for s in self.syntax:
				cats.append((self.total_alpha_syn(s),s))
				
			cats.sort()
			cats.reverse()
			if cats!=[]:
				alpha_max = cats[0][0]
			
			
			for item in cats:#set2:
				if item[0] > alpha_max/50 and len(final_set) < 20:
					
					sem = self.lex[self.syntax[item[1]][0]].sem.copy()
					sem.set_unk()
					final_set.append((item[0],(word,sem,item[1])))
			
					
		
		if final_set!=[]:
			return final_set
		else:
			return None
				
					
				
			
	def find_sem(self,sem):
		pass
	def find_syn(self,syn):
		pass





class lexical_item:
	def __init__(self,word,sem_key,syn):
		self.word = word
		self.sem_key = sem_key
		self.syn = syn
		self.key = (self.word,self.sem_key,self.syn)
		#self.sem_syn = {}
		self.alpha = 0
		self.count = 0
		self.prior = 0
		self.derivation_prob = 0
		
	def increment_count(self,lexicon):
		self.count = self.count+1
		## need to increment sem_lex | sem_c
	def reset_count(self):
		self.count = 0
		self.prior = 0
		self.derivation_prob = 0
	def print_use(self):
		print '\n<',self.word,',',self.sem,',',self.syn,'> seen ',self.count,' times'
	def set_word_prior(self):
		no_char = len(self.word) - self.word.count(' ')
		w_prior = pow((float(1)/24),no_char)
		return w_prior
		
	def update_alpha(self,alpha):
		self.alpha = self.alpha+alpha
		
	def print_alpha(self,out):
		print >> out,'<',self.word,',',self.sem,',',self.syn,'>   ::  a = ',self.alpha
#
