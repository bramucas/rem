from itertools import product


def remove_subsumed(complete_reason):  #function that removes the subsumed clauses

    

    for i in range(0, len(complete_reason)):
        for j in range(0, len(complete_reason)):
            if complete_reason[i] == set():

                pass

            elif complete_reason[i] == complete_reason[j] and i == j:

                pass

            elif complete_reason[i] == complete_reason[j] and i != j:

                complete_reason[j] = set()

            else:

                if complete_reason[i].issubset(complete_reason[j]):

                    complete_reason[j] = set()

    return [con for con in complete_reason if con != set()]



class complete_explain: #class to manage the sufficient and necessary reasons

    def __init__(self, complete_explanation):

        self.complete_explanation = complete_explanation

    def __iml(self,delta): 
        
        l = []
        min_len = []

        if len(delta) == 1:
            return delta

        else:
            for clause in delta:
                l.append((len(clause),clause))

        l.sort(key = lambda x: x[0])
        shortest_length = min(l)[0]

        for lit in l:
            if lit[0] == shortest_length:
                min_len.append(lit[1])

        return min_len
    

    def necessary_reason(self):

        if len(self.complete_explanation) == 1:
            return self.complete_explanation

        else:
            return self.__iml(self.complete_explanation)

    def sufficient_reason(self,k):


        suf_reasons = product(*self.complete_explanation)
        output = []

        if type(k) == bool:
            return [set(com) for com in suf_reasons]
        else:
            if k == 0:
                return None
            else:
                for i in range(0,k):
                    try:
                        output.append(set(next(suf_reasons)))
                    except:
                        break

                return output














