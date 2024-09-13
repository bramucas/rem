# Rem
REasoned Models: a tool for explaining ML models outcome


## References

1. Darwiche, A., & Chunxi, Ji. (2022). On the Computation of Necessary and Sufficient Explanations
. 

2. Darwiche, A., & Chunxi, Ji. (2023). A New Class of Explanations for Classifiers with
Non-Binary Features


## /rem content

Except for the dectree.py file, the rest of the files are simply auxiliary to carry out the main algorithms found in dectree.py


> - `Interval.py`: It has the class necessary to manage the literals related to the decision tree
> - `auxfunc.py`: Contains some class definition to manage the necessary and the sufficient reason from a complete reason
> - `dectree.py`: Here relies the algorithms to compute the complete reason and the general reason from a decision tree
> - `deep_search.py`: It only contains the implementation of the DFS algorithm for searching all the vertices of a decision graph

## Install

## Input format

You have to provide only the object from scikit-learn that represent your decision tree. 
 
An example procedure will be the following: 

```python

from rem import dectree as rt


dt_model = DecisionTreeClassifier() #this is your decision tree

#you have to pass this variable to the "DecisionTree" class found in dectree.py

decision_tree = rt.DecisionTree(dt_model) #the only purpose of this class is to encode the 	literals obtained from your decision tree


```
To obtain explanations to the decisions made, you will have to save the variable "decision_tree" for future uses.

## Usage

If you want to see the corresponding variables associated with each feature of your decision tree, then just print the internal variable of the object decision_tree:

```python

print(decision_tree.variables)
```


## Explanations


You have to define the corresponding objects to compute the explanations... 

```python

from rem import dectree as rt

decision_tree = rt.DecisionTree(dt_model) 

instance = [1,2,3,4,5,6,7] #has to be mandatorily in a format of type list

final_prediction = 1 #or 0 if the classifier it's binary, or any other integer if it's multi-class.

explanation = rt.Explain(decision_tree, instance, final_prediction) #this is not explanation yet.

```

### `Complete reason`

If you want simply to compute the complete reason for the decision:

```python

explanation.complete_reason()

```
However, this expression will be completely meaningless, so to have the result formatted into text, just add:

```python

explanation.complete_reason(output_text = True) 

```

**Note that this procedure it's a very expensive one, if the magnitude of the complete reason exceeds some limits.**

So if you want only the complete reason without the subsumed clauses and without any formatted text, to work with the remianing clauses, then:

```python
explanation.complete_reason(simplify = True)
```

#### `Sufficient reasons`

In this case you work also with the complete reason, but you just simply apply the distributive rule over the literals in the clauses to obtain the prime implicants.

If you want to obtain all the sufficient reasons for a certain explanation:

```python

explanation.complete_reason(sufficient_reason = True)

```
**¡Careful! This has exponential complexity** 

So if you want only just a finite number of sufficient reasons:

```python

explanation.complete_reason(sufficient_reason = k) #where k is a natural number 
```

#### `Necessary reasons`

The necessary reason can be obtained much more efficiently that the sufficient reasons. So in this case, the implementation only gives you the shortest ones (i.e the ones that has the minimum number of literals).

If you want to compute all the **shortest necessary reasons**:

```python
explanation.complete_reason(necessary_reason = True)

```

#### `Necessary and sufficient reasons`

If you want to compute all the shortest necessary reasons and the sufficient reasons for the decision:

```python
explanation.complete_reason(sufficient_reason = True, necessary_reason = True)
```

If you want only to obtain just a finite number of sufficient reasons and the shortest necessary reasons:

```python
explanation.complete_reason(sufficient_reason = k, necessary_reason = True)

```

### `General reason`

This implements all the functionalities seen in the complete_reason.

If you want to compute just simply the general reason:

```python

explanation.general_reason()
```
However, as the same as the complete, this it's completely meaningless.

If you want te **general reason formatted into text**:

```python

explanation.general_reason(output_text = True)
```
This procedure it's also, a very expensive one, so if you want only the general reason without the subsumed clauses:
```python
explanation.general_reason(simplify = True)
```