from rem.deep_search import *
import copy
from rem.Interval import *
from rem.auxfunc import *



class explain:


	def __init__(self, dec_tree, instance, decision):



		self.dec_tree = dec_tree
		self.instance = instance
		self.decision = decision
		

		try:
			if type(self.instance) != list or self.instance is None:
				raise TypeError
			elif 0 <= len(self.instance) < self.dec_tree.dt_model.n_features_in_:
				raise ValueError
		except TypeError:
			print("El formato de instancia no es valido.")	
		except ValueError:
			print("Instancia no valida")

		else:
			self.__instance_to_literals()


	def show_instance(self): #show the corresponding literals to the values of the instance

		for index in range(0,len(self.instance)):
			print(f"{self.dec_tree.name_vars[index]} in {self.instance[index]}\n")


	
	def __instance_to_literals(self): #translate the values of the instance to the literals of the decision tree

		for i in range(0,len(self.instance)):
			for clave, valor in self.dec_tree.variables[i].items():
				if self.instance[i] in valor:
					self.instance[i] = valor 
					break 

	

	def __output_text(self, cnf):  #text output for the complete and general reason

		try:
			if len(cnf) >= 200:
				raise valueError
		except:
			print("Value too long to be printed")

		for index in range(0,len(cnf)):
			print(f"{index+1} clause:\n")
			for lit in cnf[index]:
				print(f"{self.dec_tree.name_vars[lit.feature]} in {lit}")
			print("\n")

	


	def __output_text_nr(self, formula): #text output for the necessary reason
		
		try:
			if len(formula) >= 200:
				raise ValueError
		except:
			print("Value too long to be printed")
		
		for index in range(0,len(formula)):	
			print(f"{index+1} necessary reason:\n")
			for lit in formula[index]:
				print(f"{self.dec_tree.name_vars[lit.feature]} in {lit}")
			print("\n")

	


	def __output_text_sr(self, formula): #text output for the sufficient reason

		try:
			if len(formula) >= 200:
				raise ValueError

		except:
			print("Value too long to be printed")

		for index in range(0,len(formula)):
			print(f"{index+1} sufficient reason:\n")
			for lit in formula[index]:
				print(f"{self.dec_tree.name_vars[lit.feature]} in {lit}")
			print("\n")





	def complete_reason(self, simplify = None, output_text = None, sufficient_reason = None, necessary_reason = None): #complete reason

		complete_reason = []


		for path in DFC(self.dec_tree.dt_model):

			if self.dec_tree.dt_model.tree_.value[path[-1]].flatten().argmax() == self.decision: #si la decision de un camino, es nuestra decision, ignoramos el camino
				pass
			else:

				product = set() #clausula asociada a un camino

				for index in range(0, len(path)): 
					if index == len(path) - 1:     
						break

					feature = self.dec_tree.dt_model.tree_.feature[path[index]]
					literal = self.instance[feature] 
					threshold = self.dec_tree.dt_model.tree_.threshold[path[index]]


					if path[index + 1 ] == self.dec_tree.dt_model.tree_.children_left[path[index]]: #main algorithm
						if literal.sup <= threshold:
							pass
						else:
							product.add(literal) 

					elif path[index + 1 ] == self.dec_tree.dt_model.tree_.children_right[path[index]]:
						if literal.sup > threshold:
							pass
						else:
							product.add(literal)

				complete_reason.append(product) 



		if sufficient_reason is not None or necessary_reason is not None:

			if (sufficient_reason is False or sufficient_reason is None) and necessary_reason is True:
				return self.__output_text_nr(complete_explain(remove_subsumed(complete_reason)).necessary_reason())

			elif (sufficient_reason is True or type(sufficient_reason) == int) and (necessary_reason is False or necessary_reason is None):
				return self.__output_text_sr(complete_explain(remove_subsumed(complete_reason)).sufficient_reason(sufficient_reason))

			elif sufficient_reason is not None and necessary_reason is True:
				self.__output_text_sr(complete_explain(remove_subsumed(complete_reason)).sufficient_reason(sufficient_reason))
				print("\n\n")
				return self.__output_text_nr(complete_explain(remove_subsumed(complete_reason)).necessary_reason())
		else:
			if output_text == True:
				return self.__output_text(remove_subsumed(complete_reason))
			elif simplify == True:
				return remove_subsumed(complete_reason)
			else:
				return complete_reason

		

		
	def general_reason(self, simplify = None, output_text = None): #general reason


	    general_reason = []

	    for path in DFC(self.dec_tree.dt_model):
	      if self.dec_tree.dt_model.tree_.value[path[-1]].flatten().argmax() == self.decision:
	        pass
	      else:
	        product = set()

	        for index in range(0, len(path)):

	          if index == len(path) - 1:
	            break

	          else:
	            
	            feature = self.dec_tree.dt_model.tree_.feature[path[index]]
	      
	            literal = self.instance[feature]
	            literals = self.dec_tree.variables[feature]

	            threshold = self.dec_tree.dt_model.tree_.threshold[path[index]]

	            if path[index + 1] == self.dec_tree.dt_model.tree_.children_right[path[index]]: #main algorithm

	              if literal.sup > threshold:
	                pass
	              else:
	                for clave, val in literals.items():
	                  if val.sup <= threshold:
	                    product.add(val)            

	            elif path[index +1]  == self.dec_tree.dt_model.tree_.children_left[path[index]]:

	              if literal.sup <= threshold:
	                pass
	              else:
	                for clave, val in literals.items():               
	                  if val.sup > threshold:
	                    product.add(val)
	          
	        general_reason.append(product)



	    if output_text == True:
	    	return self.__output_text(remove_subsumed(general_reason))
	    elif simplify == True:
	    	return remove_subsumed(general_reason)
	    else:
	    	return general_reason

	    

	 	



class decisionTree:

	variables = []

	def __init__(self, data_dict):

		self.dt_model = data_dict['model']
		self.name_vars = data_dict['feature_names']

		for i, fname in enumerate(self.name_vars):
			self.variables.append(self.__discretize(i,data_dict['model']))

	
	def __discretize(self, feature ,dt_model): #it codifies all the variables of the tree into discrete literals

		temp_list = set()
		literal_dict = {}
		

		for i in range(0, dt_model.tree_.node_count):
			if dt_model.tree_.feature[i] == feature:
				temp_list.add(dt_model.tree_.threshold[i])

		temp_list = list(temp_list)
		temp_list.sort()

		len_threshold = len(temp_list)

		if len_threshold == 1: #boolean variable
			literal_dict[1] = Interval(-oo,temp_list[0], feature = feature)
			literal_dict[2] = Interval(temp_list[0],+oo, left_open = True, feature = feature)


		else:	#looking for an optimized method
			for i in range(0,len_threshold): 
				if i == (len(temp_list) - 1):
					literal_dict[i+1] = Interval(temp_list[i-1],temp_list[i],left_open = True, feature = feature) 
					literal_dict[i+2] = Interval(temp_list[i], +oo, left_open = True, feature = feature)

				if 0 < i < (len(temp_list) - 1):
					literal_dict[i+1] = Interval(temp_list[i-1],temp_list[i], left_open = True, feature = feature)

				if i == 0:  
					literal_dict[1] = Interval(-oo, temp_list[0], feature = feature) 


		return literal_dict   




        


