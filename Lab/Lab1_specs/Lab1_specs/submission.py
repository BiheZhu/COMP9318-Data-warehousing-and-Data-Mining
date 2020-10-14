## import modules here 

################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    for i in range(0, x//2):
        if i*i <= x:
            result = i
            continue
        else:
            return result


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    x_new = x_0 - f(x_0) / fprime(x_0)
    x_old = x_0
    for i in range(1, MAX_ITER):
        if abs(x_old - x_new) < EPSILON:
            return x_new
        else:
            temp = x_new
            x_new = temp - f(temp) / fprime(temp)
            x_old = temp


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree(tokens): # do not change the heading of the function
    result = ""
    for i in range(0, len(tokens)):
        if tokens[i] == '[':
            result += ',['
        if tokens[i] == ']':
            if i < len(tokens) - 1:
                if tokens[i+1] != ']':
                    result += ")]), "
                if tokens[i+1] == ']':
                    result += ")]"
            else:
                result += ")])"
        if tokens[i] not in {'[', ']'}: 
            if tokens[i+1] not in {'[', ']'}:
                #result += f"Tree('{tokens[i]}'),"
                result = result + "Tree('" +tokens[i] + "'),"
            else:
                #result += f"Tree('{tokens[i]}'"
                result = result + "Tree('" +tokens[i] + "'"
    return eval(result)    

def max_depth(root): # do not change the heading of the function
    height = []
    if root.children == []:
        return 1
    else:
        for i in root.children:
            Depth = max_depth(i)
            height.append(Depth)
        return max(height)+1
