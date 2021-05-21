class Node:
    '''The basic structure that keeps Node and Leafs'''
    def __init__(self, newdata):
        '''Initialize empty data object'''
        self.data = newdata
        '''basic data'''
        self.is_leaf = self.checkData()
        '''Marker indicates whether it is a leaf or node'''
        self.right = None
        self.left = None
    def checkData(self):
        node_sign = ["*",  "|", "+", "?", "(", ")"]
        for i in node_sign:
            if self.data == i:
                return False
        return True
    def __str__(self):
        return self.data

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
                while (op and (op[-1].data > buffer.data)):
                    #powyzsze stwierdzenie jest bledne,
                    #chodzi o to jaki to ma precedence
                    #to musi byc teraz zrobione!!!!!!!!!!!!!!!
                #go to the point 2) and do all subpoints of 2)
    while op:
        output.append(op.pop())
    for i in output:
        print(i)
#                if not op:
    #use empty symbol if no operator is needed

class SyntaxTree:
    def __init__(self):
        self.root = Node("")
    def insert(self, char):
        self.root.data = "Delete this line pls"
