from sympy import oo

class Interval:

	def __init__(self, left, right, var, rightOpened = True, leftOpened = True):
		
		self.left = left
		self.right = right
		self.var = var 
		self.rightOpened = rightOpened
		self.leftOpened = leftOpened

		if(left >= right):
			raise ValueError("Invalid args for interval")

	def __hash__(self):

		return hash((self.left, self.right, self.var))
		
	def __eq__(self, comp):

		if isInstance(comp, Interval):
			return (self.left, self.right, self.var) == (self.left, self.right, self.var)
		return False	

	def __contains__(self, x):
			
		if(not self.rightOpened and not self.leftOpened):
			return self.left <= x <= self.right
		elif(not self.rightOpened and self.leftOpened):
			return self.left <= x < self.right
		elif(self.rightOpened and not self.leftOpened):
			return self.left < x <= self.right
		else:
			return self.left < x < self.right


	def __str__(self):
			if(not self.rightOpened and not self.leftOpened):
				return f"[{self.left},{self.right}]"
			elif(not self.rightOpened and self.leftOpened):
				return f"[{self.left},{self.right})"
			elif(self.rightOpened and not self.leftOpened):
				return f"({self.left},{self.right}]"
			else:
				return f"({self.left},{self.right})"

	def intersect(self, other):

		leftside = max(self.left, other.left)
		rightside = min(self.right, other.right)

		if(self.left != other.left):
			if(other.left > self.left):
				self.leftOpened = other.isLeftOpened()
		else:
			self.leftOpened = self.leftOpened or other.isLeftOpened()

		if(self.right != other.right):
			if(self.right > other.right):
				self.rightOpened = other.isRightOpened()
		else:
			self.rightOpened = self.rightOpened or other.isRightOpened()

		self.left = leftside
		self.right = rightside			

	def leftOpen(self, cond):
		self.leftOpened = cond

	def rightOpen(self, cond):
		self.rightOpened = cond
					

	def isLeftOpened(self):
		return self.leftOpened
	
	def isRightOpened(self):
		return self.rightOpened
				
