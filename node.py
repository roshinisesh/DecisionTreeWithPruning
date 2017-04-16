class Node:
    value = ""
    children = []        
    parentLis = []
    def __init__(self, val, dictionary, substitution = None, ID = None):   
        if substitution is None:
            substitution = ""
        
        if ID is None:
            ID = ""

        self.value = val
        self.children = dictionary   
        self.ReplaceName = substitution
        self.setTheId = ID
        self.value = val
        
    def __str__(self):
        return str(self.value), str(self.ReplaceName),str(self.setTheId)
    


        