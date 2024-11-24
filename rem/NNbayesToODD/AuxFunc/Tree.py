class Node:

	def __init__(self, labelVar, rightChild, leftChild):

		self.labelVar = labelVar
		self.rightChild = rightChild
		self.leftChild  = leftChild


	def __hash__(self):
		return hash((self.labelVar, self.rightChild, self.leftChild))

	def __eq__(self, other):
	
		if(isinstance(other, Node)):
			return (self.labelVar, self.rightChild, self.leftChild) == (self.labelVar, self.rightChild, self.leftChild)
		return False

	def isLeaf(self):
		return self.rightChild == None and self.leftChild == None		

	def addRightChild(self, rightChild):
		self.rightChild = rightChild	

	def addLeftChild(self, leftChild):
		self.leftChild = leftChild	

	def RightChild(self):
		return self.rightChild
	def LeftChild(self):
		return self.leftChild
	def LabelVar(self):
		return self.labelVar			