# this reads in the smeantic templates from a file

class template:
	def __init__(self,name,type,args):
		self.name = name
		self.type = type
		for arg in self.args:
			args.append(
