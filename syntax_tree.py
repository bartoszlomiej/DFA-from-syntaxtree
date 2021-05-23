class Node:
    '''The basic structure that keeps Node and Leafs'''
    def __init__(self, newdata):
        '''Initialize empty node/leaf object'''
        self.data = newdata #keeps the character
        self.is_leaf = self.check_data()#Marker indicates whether it is a leaf or node
        self.right = None
        self.left = None
    def check_data(self):
        '''Checks whether given char is a node or a leaf'''
        node_sign = ["*",  "|", "+", "?", "(", ")"]
        for i in node_sign:
            if self.data == i:
                return False
        return True
    def __str__(self):
        '''To print the data i convenient way'''
        return self.data

def RegExpToString(exp):
    '''Converts the string to the another notation - the concatenation symbol will be the '.' so a make to easier in later conversion to the Postfix notation'''
    operator = ["*",  "|", "+", "?", "(", ")"]
    output = []
    for i in operator:
        if exp[0] == i and i != '(': #if the expression is started with another operator, then it must be wrong.
            return -1
    counter = 0
    for i in exp:
        marker = False
        if counter > 0:
            for o in operator:
                if o == i or o == exp[counter - 1]:
                    marker = True
            if not marker:
                output.append(".")
        output.append(i)
        counter = counter + 1
    return output
        
        
        

def RegExp2Postfix(exp):
    '''Converts the regular expression to the postfix notation

    The Shunting yard algorithm is implemented so as to convert the regular expression into the postfix notation.
    '''
    #a.(b|d)* -> abd |.*
    #a.b.c* -> ab.c*
    #a.(b|d).c* -> abd|.c*.
    #assumptions:
    #-the sign is attach to the 2 previous expressions if it is |
    #-the sign is attach to the 1 previous expressions if it is *, +, ?
    #-() groups the in between expressions into one expression
    #algorithm:
    # 1) if it is symbol -> append to output
    # 2) elif it is special character:
    # 2.1) while there is a character on the operator stack and (the operator on the top of the operator stack has the greater precedence or (the operator on the top has equal precedence and the opeartor at the top is left associative)) and operator at the top is not left parenthesis:
    # 2.1.1) pop operators from opeartor stack and attach them to the output
    # 2.2) push it onto the operator stack
    # 3) elif it is left parenthesis:
    # 3.1) push it onto the operators stack
    # 4) elif it is right parenthesis:
    # 4.1) while the operator at the top is not left parenthesis:
    # 4.1.1) pop the operator from the operators stack to the output
    # 4.2) if there is left parenthesis at the top of operator stack:
    # 4.2.1) pop the operator from the operator stack and discard it
    # 5) if there are no more token to read:
    # 5.1) while there are operators on the operator stack:
    # 5.1.1) pop them and attach to the output
    output = []
    op = []
#    precedence = {'*':0,'?':0, '+':0, '|':1 }
#the '' - denotes the concatenation???
#only the or operator have the smallest precedence
#all operators are left associative

    for i in exp:
        buffer = Node(i)
        if buffer.is_leaf:
            output.append(buffer)
        else:
            if buffer.data == "(":
                op.append("(")
            elif buffer.data == ")":
                while op[-1] != "(":
                    output.append(op.pop())
                if op[-1] == "(":
                    op.pop()
            else:
                while (op and ((op[-1] == '|' and buffer.data == '|') or op[-1] != '|') and op[-1] != '('):
                    output.append(op.pop())
                op.append(buffer.data)
    while op:
        output.append(op.pop())
    for i in output:
        print(i)
#                if not op:
    #use empty symbol if no operator is needed

class SyntaxTree:
    '''This class is a data structure that keeps the regular expression as a Syntax Tree.
    '''
    def __init__(self):
        self.root = Node("")
    def insert(self, char):
        self.root.data = "Delete this line pls"
