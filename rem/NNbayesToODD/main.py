import numpy as np
from AuxFunc import *
from sklearn.naive_bayes import BernoulliNB




class NaiveBayesToOdd: #representa el procedimiento de pasar de naive bayes a odd



	def __init__(self, model):
		self.model = model
		self.num_vars = model.n_features_in_

		self.cache = [{} for n in range(0, model.n_features_in_)]


	def __find_in_cache(self, num_cache, prob):
	
		for clave, valor in self.cache[num_cache].items():
			if prob in clave:

				print(f"{clave}:{valor}\n")
				return (clave, valor)



		return None			

	def	__store_in_cache(self, num_cache, interval, node):
		self.cache[num_cache][interval] = node 

	def __offset(self, interval, weight):

		return Interval(interval.left + weight, interval.right + weight, 
			interval.var, rightOpened = interval.isRightOpened(), leftOpened = interval.isLeftOpened())


		 	


	def build_odd(self, threshold):

		threshold_log_odd = np.log(threshold/(1-threshold))

		prob = np.exp(self.model.class_log_prior_[1])
		log_prob_odd = np.log(prob/(1-prob))


		Sink_1 = Node("clase 1", None, None)
		Interval_Sink_1 = Interval(threshold_log_odd, oo, "clase 1", leftOpened = False)
		self.__store_in_cache(self.num_vars-1, Interval_Sink_1, Sink_1)
		Sink_0 = Node("clase 0", None, None)
		Interval_Sink_0 = Interval(-oo, threshold_log_odd, "clase 0")
		self.__store_in_cache(self.num_vars-1, Interval_Sink_0, Sink_0)


		return self.__Build_Sub_Odd(0, log_prob_odd)

	def __Build_Sub_Odd(self, k, prob):

		probabilities = self.model.feature_log_prob_
		nodeVar = Node(f"Var {k}", None, None)
		intervalVar = Interval(-oo, oo, f"Var {k}")

		print(k)
		for i in range(0,2):
 
			if(i == 1):
				weight_of_evidence = probabilities[1][k+1] - probabilities[0][k+1]
			else:
				weight_of_evidence = np.log(1-np.exp(probabilities[1][k+1])) - np.log(1 - np.exp(probabilities[0][k+1]))

			prob_child = prob + weight_of_evidence
			node_child_aux = self.__find_in_cache(k+1, prob_child)


			if(node_child_aux != None):
				node_child = node_child_aux[1]
				node_child_interval = node_child_aux[0]

			else: 
				node_child_aux = self.__Build_Sub_Odd(k+1, prob_child)
				node_child = node_child_aux[0]
				node_child_interval = node_child_aux[1]

			try:	
				if(i == 1):
					nodeVar.addRightChild(node_child)
				else:
					nodeVar.addLeftChild(node_child)
			except Exception as e:
				print(e, node_child)
						

			intervalVar.intersect(self.__offset(node_child_interval,-weight_of_evidence))

		self.__store_in_cache(k, intervalVar, nodeVar)
		return (nodeVar, intervalVar)



			
		






	
