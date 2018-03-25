import copy
global filename
class Soduku:
	def __init__(self,filename):
		file = open(filename,"r")
		lines = file.readlines()
		a=[] 
		b=[] # to store the numbers
		assign=[] # whether fixed, uncertain, or empty
		probly=[] # store all possible digits for each blank
		problyCNT=[] # number of possibilities for each blank
		location=[] # stores row,col,boxIdx of each blank
		level=0
		for i,line in enumerate(lines):
			a.append(line)
		for i in range(9):
			for j in range(9):
				b.append(int(a[i][j]))
				b_row=int(i/3)
				b_col=int(j/3)
				bidx=3*b_row+b_col
				location.append([i,j,bidx])
				if a[i][j]=='0':
					assign.append(0)
					probly.append([1,2,3,4,5,6,7,8,9])
					problyCNT.append(9)
				else:
					assign.append(1)
					probly.append([int(a[i][j])])
					problyCNT.append(1)
		self.matrix=b
		self.probly=probly
		self.problyCNT=problyCNT
		self.assign=assign
		self.location=location
		self.level=level
	def set_matrix(self,matrix):
		self.matrix=matrix
		# print(matrix)
	def set_probly(self,probly):
		self.probly=probly
		
	def set_assign(self,assign):
		self.assign=assign
	def set_problyCNT(self,problyCNT):
		self.problyCNT=problyCNT
	def set_location(self,location):
		self.location=location
	def set_level(self,lvl):
		self.lvl=lvl
	def update(self,problyCNT,probly):
		'''
		problyCNT,assign,probly,matrix
		'''
		self.set_problyCNT(problyCNT)
		# self.set_assign(assign)
		self.set_probly(probly)
		# self.set_matrix(matrix)

	def Optimize(self):
		# print('Optimizing')
		probMat=copy.copy(self.probly)
		for i in range(81): # reset the possibilities mat
			if self.assign[i]!=1:
				probMat[i]=[1,2,3,4,5,6,7,8,9]
		self.set_probly(probMat)
		for i in range(81):
			CNTmat=copy.copy(self.problyCNT)
			Promat=copy.copy(self.probly)
			if self.assign[i]==1:
				CNTmat[i]=1
				Promat[i]=[self.matrix[i]]
				self.update(CNTmat,Promat)
				# print(i,self.assign[i],self.probly[i])
			else:
				for j in range(81):
					if j!=i and self.assign[j]==1:
						locj=self.location[j]
						loci=self.location[i]
						if (locj[0]-loci[0])*(locj[1]-loci[1])*(locj[2]-loci[2])==0:
							suredValue=self.matrix[j]
							if suredValue in self.probly[i]:
								problyNow=copy.copy(self.probly)
								problyCNTNow=copy.copy(self.problyCNT)
								del problyNow[i][problyNow[i].index(suredValue)]
								problyCNTNow[i]=len(problyNow[i])
								# print('remove',suredValue,'from',loci,'due to',locj)
								if problyCNTNow[i]==0:
									# print(self.probly)
									# print('row107 error occur at',i, 'roll back, level',self.level)
									return None
								else:
									self.update(problyCNTNow,problyNow)
				# print(i,self.probly[i])
		return self
	
	def checkPossibility(self):
		# update the matrix by excluding impossible options
		# print('checkingPossibility')
		assure_count=sum(self.assign)
		if assure_count==81:
			return True
		else:
			for i in range(81):
				loci=self.location[i]
				if self.assign[i]==1:
					for j in range(81):
						locj=self.location[j]
						if j!=i and (loci[0]-locj[0])*(loci[1]-locj[1])*(loci[2]-locj[2])==0:
							if self.matrix[i]==self.matrix[j]:
								# print('conflicting',loci,locj,self.matrix[j])
								return False
			return True
	def GetMinP(self):
		minP=10
		MinPIdx=81
		for i in range(81):
			if self.problyCNT[i]<minP and not self.assign[i]:
				minP=self.problyCNT[i]
				MinPIdx=i
		# print('minP',minP,' at ',self.location[MinPIdx],' possibilities are:',self.probly[MinPIdx])
		if minP==10:
			# print('solution: row123\n',self.matrix,'\nrow136 assign is\n',self.assign)
			return MinPIdx
		if minP==0:
			# print('error row126, rolling back',self.level)
			# print('',self.matrix)

			return -1
		return MinPIdx


def Solve(SodukuObj,level):
	# print('level',level,'\n',SodukuObj.matrix)
	cpy=copy.copy(SodukuObj) #make backup
	if not SodukuObj.checkPossibility():
		# print('check possibilities failed level',level)
		return None
	else:
		if not SodukuObj.Optimize():
			return None
		if sum(SodukuObj.assign)==81:
			# print(SodukuObj.matrix)
			return SodukuObj
		else: # find the joint shortest branch
			minIdx=SodukuObj.GetMinP()
			if minIdx<0: # can't get minIdx
				return None
			elif minIdx>80: # Solved
				# print(SodukuObj.matrix)
				return SodukuObj
			else:# solve cloned new matrix with new value
				for probability in SodukuObj.probly[minIdx]: 
					mat=copy.copy(SodukuObj.matrix)
					ass=copy.copy(SodukuObj.assign)
					mat[minIdx]=probability
					ass[minIdx]=1
					SodukuObj.set_matrix(mat)
					SodukuObj.set_assign(ass)
					SodukuObj.set_level(level+1)
					if Solve(SodukuObj,level+1)!=None:
						return SodukuObj
				SodukuObj.set_matrix(copy.copy(cpy.matrix))
				SodukuObj.set_assign(copy.copy(cpy.assign))
				SodukuObj.set_level(level)
				SodukuObj.Optimize()
				return None

filename='Soduku.txt'
shudu=Soduku(filename)
solution=Solve(shudu,0)
if solution!=None:
	print (solution.matrix)
else:
	print('failed to solve')