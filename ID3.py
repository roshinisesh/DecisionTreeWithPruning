from node import Node
import math
import copy
import random
import string 
from random import choice

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node) 
    trained on the examples.  Each example is a dictionary of attribute:value pairs,
    and the ClassIndexAttr class variable is a special attribute with the name "Class".
    Any missing attributes are denoted with a value of "?"
    '''
    attributes = examples[0].keys()
    data = []
    for Iteration in examples:
        data.append(Iteration.values())  
    ClassIndexAttr = "Class"
    data = data[:]
    column = [content[attributes.index(ClassIndexAttr)] for content in data]
    default2 = SpecialCase(attributes, data, ClassIndexAttr)
    if not data or (len(attributes) - 1) <= 0:
        return default2
    elif column.count(column[0]) == len(column):
        return column[0]
    else:
        [best,calcuclass] = BestAttr(data, attributes, ClassIndexAttr)
        tree = {best:{}}
        for val in GetOpt(data, attributes, best):#val is numb now
            expl2 = GetNewSubdata(data, attributes, best, val)#val is numb now
            NewAttribute = attributes[:]
            NewAttribute.remove(best)
            examples3 = []           
            for i in range(0,len(expl2)):
                temp2 = {NewAttribute[j]:expl2[i][j] for j in range(0,len(NewAttribute))}
                examples3.append(temp2)                
            NodeDictSmall = {"initial":0}            
            dataSubset_LastOne = [Iteration[-1] for Iteration in expl2]
            for variable in dataSubset_LastOne:
            	maxNumb = dataSubset_LastOne.count(variable)
            	if maxNumb > NodeDictSmall.values()[0]:
            		NodeDictSmall.clear()
            		NodeDictSmall[variable] = maxNumb            
            substitution = NodeDictSmall.keys()[0]     
            subtree = ID3(examples3, default)
            ID =random_char(5)
            valNode = Node(val,subtree,substitution,ID)            
            tree[best][valNode] = subtree      
    return tree            


def prune(node, examples):                    
        
    '''
    Takes in a trained tree and a validation set of examples.  Prunes nodes in order
    to improve accuracy on the validation data; the precise pruning strategy is up to you.
    '''    
    NameList = []
    Output = walk(node, NameList)
    node_tem = copy.deepcopy(node)
    Output2 = [Iteration for Iteration in Output]
    count = 0
    node_final = {}
    for Iteration in Output2:
        count += 1
        if isinstance (node_tem, dict):  
            node_tem = ReplaceBestSubTree(Iteration,node_tem)  
        error = get_error(node_tem,examples)#Output2 is pruned, examples is validataion data
        if count == 1:
            error_min = error
            node_final = copy.deepcopy(node_tem)
        else:                 
            if error < error_min:
                error_tmp = error
                name = Iteration
                node_final = copy.deepcopy(node_tem)
        node_tem = copy.deepcopy(node)        
    return node_final


def test(node, examples):    
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''    
    error = get_error(node,examples)
    acc = 1-error
    return acc
    

def evaluate(node, example):
    '''
    Takes in a tree and one example.  Returns the Class value that the tree
    assigns to the example.
    '''
    data = [example]
    attributes = data[0].keys()
    examples = []
    hahaName = "Initial"
    for Iteration in data:
        examples.append(Iteration.values())      
    if isinstance(node, dict):
        count = 0
        for Iteration in examples:
            count += 1
            Tem_Dictionary = copy.deepcopy(node)
            while(isinstance(Tem_Dictionary, dict)):
                Tem_DictionaryKeys = Tem_Dictionary.keys()[0]
                Tem_Dictionary = Tem_Dictionary[Tem_DictionaryKeys]
                if isinstance(Tem_Dictionary,dict):                    
                    Tem_Dictionary_val_tmp = Tem_Dictionary.keys()                                       
                    index = attributes.index(Tem_DictionaryKeys)
                    value = Iteration[index]
                    
                    Tem_DictionaryValList = [Iteration2.value for Iteration2 in Tem_Dictionary_val_tmp]
                    if Tem_DictionaryValList.count(value)==0:
                        result = hahaName
                        return result
                    else:         
                        for tmp in Tem_Dictionary_val_tmp:
                            Tem_Dictionary_val = tmp.value
                            if tmp.value == value:
                                    result = Tem_Dictionary[tmp]
                                    hahaName = tmp.ReplaceName
                                    Tem_Dictionary = Tem_Dictionary[tmp]
                                    break
    else:
        result = node        
  
    return result


def ReplaceBestSubTree(Iteration,tree):#path is the dictionary, FinalDict 
    if isinstance(tree, dict):
        sub_dict = tree.values()[0]
        for child in sub_dict:
            if isinstance(child,Node):
                sub_sub_dict = sub_dict[child]                   
                if child.setTheId == Iteration:
                    sub_dict[child] = child.ReplaceName  
                    break
                else:
                    ReplaceBestSubTree(Iteration,sub_sub_dict) 
            else:
                pass
    else:
        tree = tree                                    
    return tree


def get_error(tree,validation_data):
    error = 0.0
    count = 0
    for Iteration2 in validation_data:
        count = count+1
        Iteration = copy.deepcopy(Iteration2)
        label = Iteration.pop("Class")
        e_result = evaluate(tree, Iteration)
        if label == e_result:
            pass
        else:
            error += 1      
    error = error/count
    return error
    

def walk(name, NameList):#walk(node(the whole tree), NameList)
    if isinstance(name, dict):
        for child in name:
            if isinstance(child,Node):
                pass                          
            else:                
                Key = name.values()[0]    
                for Iteration in Key:
                    NameList.append(Iteration.setTheId)
                    HaiZi = Key[Iteration]
                    walk(HaiZi,NameList)
    else:
         pass
    return NameList


def SpecialCase(attributes, data, ClassIndexAttr):
    EleFrequency = {}
    index = attributes.index(ClassIndexAttr)
    for tuple in data:
        if (EleFrequency.has_key(tuple[index])):
            EleFrequency[tuple[index]] += 1 
        else:
            EleFrequency[tuple[index]] = 1
    max = 0
    major = ""
    for key in EleFrequency.keys():
        if EleFrequency[key]>max:
            max = EleFrequency[key]
            major = key
    return major


def entropy(attributes, data, ClassIndexAttrAttr):
    EleFrequency = {}
    dataEntropy = 0.0
    i = 0
    for Iteration in attributes:
        if (ClassIndexAttrAttr == Iteration):
            break
        i = i+1
    for Iteration in data:
        if (EleFrequency.has_key(Iteration[i])):
            EleFrequency[Iteration[i]] += 1.0
        else:
            EleFrequency[Iteration[i]]  = 1.0    
    for Frequency in EleFrequency.values():
        dataEntropy += (-Frequency/len(data)) * math.log(Frequency/len(data), 2)  
    return dataEntropy


def InfoGain(attributes, data, attr, ClassIndexAttrAttr,calcuclass):
    EleFrequency = {}
    subsetEntropy = 0.0
    NodeDictSmall = {"initial":0}
    i = attributes.index(attr)
    for Iteration in data:
        if (EleFrequency.has_key(Iteration[i])):
            EleFrequency[Iteration[i]] += 1.0
        else:
            EleFrequency[Iteration[i]]  = 1.0
    for val in EleFrequency.keys():
        valProb        = EleFrequency[val] / sum(EleFrequency.values())
        dataSubset     = [Iteration for Iteration in data if Iteration[i] == val]
        dataSubset_LastOne = [Iteration[-1] for Iteration in dataSubset]
        for variable in dataSubset_LastOne:
            maxNumb = dataSubset_LastOne.count(variable)
            if maxNumb > NodeDictSmall.values()[0]:
                NodeDictSmall.clear()
                NodeDictSmall[variable] = maxNumb
        if isinstance(val,str):
            pass
        else:
            val = str(val)        
        if attr=="Class":
            pass
        else:
            calcuclass[attr+val] = NodeDictSmall.keys()[0]
        subsetEntropy += valProb * entropy(attributes, dataSubset, ClassIndexAttrAttr)
    return (entropy(attributes, data, ClassIndexAttrAttr) - subsetEntropy),calcuclass


def BestAttr(data, attributes, ClassIndexAttr):
    attributes2 = copy.deepcopy(attributes)
    attributes2.remove("Class")
    best = attributes2[0]
    maxGain = 0;
    calcuclass = {}
    for attr in attributes:  
        if attr == "Class":
            pass
        else:
            [NewGain,calcuclass] = InfoGain(attributes, data, attr, ClassIndexAttr,calcuclass)
            if NewGain>maxGain:
                maxGain = NewGain
                best = attr
    return best,calcuclass


def GetOpt(data, attributes, attr):
    index = attributes.index(attr)
    values = []
    for Iteration in data:
        if Iteration[index] not in values:
            values.append(Iteration[index])
    return values


def GetNewSubdata(data, attributes, best, val):
    expl2 = [[]]
    index = attributes.index(best)
    for Iteration in data:
        if (Iteration[index] == val):
            newIteration = []
            for i in range(0,len(Iteration)):
                if(i != index):
                    newIteration.append(Iteration[i])
            expl2.append(newIteration)
    expl2.remove([])
    return expl2
