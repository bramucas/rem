from sympy import oo


class Interval: #class to manage the literals of the tree

    def __init__(self,inf, sup, left_open = False, right_open = False, feature = None):
        
        self.inf = inf
        self.sup = sup
        self.left_open = left_open
        self.right_open = right_open
        self.feature = feature
        
        if type(self.left_open) != bool or type(self.right_open) != bool:
            raise ValueError("Los tipos especificados deben ser booleanos")
        elif self.inf >= self.sup or self.sup <= self.inf:
            raise ValueError("Los limites superiores e inferiores no son validos")
                
        
        
        if self.inf == -oo:
            self.left_open = True
        elif self.sup == +oo:
            self.right_open = True
            
        
    def __str__(self):
        
        if self.left_open == True and self.right_open == True:
            return f"({self.inf},{self.sup})"
        elif self.left_open == True and self.right_open == False:
            return f"({self.inf},{self.sup}]"
        elif self.left_open == False and self.right_open == True:
            return f"[{self.inf},{self.sup})"
        else:
            return f"[{self.inf},{self.sup}]"
        
    
    def __contains__(self,valor):
        
        if self.left_open == True and self.right_open == True:
            return self.inf < valor < self.sup
        elif self.left_open == True and self.right_open == False:
            return self.inf < valor <= self.sup
        elif self.left_open == False and self.right_open == True:
            return self.inf <= valor < self.sup
        else:
            return self.inf <= valor <= self.sup
        
    def __hash__(self):
        return hash((self.inf, self.sup, self.feature))
    
    
    def __eq__(self, intervalo):
        
        if isinstance(intervalo, Interval):
            return intervalo.inf == self.inf and intervalo.sup == self.sup
        return False
        
        
    def union(self, intervalo):
        
        if self.contains(intervalo) or self.issubset(intervalo):
            pass
        else:
            if self.sup >= intervalo.inf and self.sup < intervalo.sup:
                self.sup = intervalo.sup
                self.right_open = intervalo.right_open
            elif intervalo.sup >= self.inf and self.sup > intervalo.sup:
                self.inf = intervalo.inf
                self.left_open = intervalo.left_open
        
    
    def issubset(self, intervalo):
        
        return intervalo.inf <= self.inf and self.sup <= intervalo.sup
    
    def contains(self, intervalo):
        
        return self.inf <= intervalo.inf and intervalo.sup <= self.sup