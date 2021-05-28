class Node:
    '''The basic structure that keeps Node and Leafs'''
    def __init__(self, newdata):
        '''Initialize empty node/leaf object'''
        self.data = newdata  #keeps the character
        self.is_leaf = self.check_data(
        )  #Marker indicates whether it is a leaf or node
        self.right = None
        self.left = None

    def check_data(self):
        '''Checks whether given char is a node or a leaf'''
        node_sign = ["*", "|", "+", "?", "(", ")", "."]
        for i in node_sign:
            if self.data == i:
                return False
        return True

    def PrintTree(self):
        print(self)

    def __str__(self):
        '''To print the data i convenient way'''
        return self.data


def RegExpToString(exp):
    '''Converts the string to the another notation - the concatenation symbol will be the '.' so a make to easier in later conversion to the Postfix notation'''
    operator = ["|", "(", ")"]
    all_operators = ["*", "|", "+", "?", "(", ")"]
    output = []
    for i in operator:
        if exp[0] == i and i != '(':  #if the expression is started with another operator, then it must be wrong.
            return -1
    counter = 0
    for i in exp:
        marker = False
        for o in operator:
            if counter + 1 < len(exp):
                if o == i or o == exp[
                        counter +
                        1]:  #check if there are two operators in the row
                    marker = True
            else:
                marker = True
        for a in all_operators:
            if counter + 1 < len(exp):
                if a != i and a == exp[
                        counter + 1]:  #check if after symbol there is operator
                    marker = True
        output.append(i)
        if not marker:
            output.append(".")
        counter = counter + 1
    return output


def check_precedence(char, top):
    '''Checks the precedence of the two characters in the regular expression'''
    precedence = {'*': 2, '?': 2, '+': 2, '.': 1, '|': 0, '(': 0}
    if precedence[char] <= precedence[top]:
        return True
    return False


def RegExp2Postfix(exp):
    '''Converts the regular expression to the postfix notation

    The Shunting yard algorithm is implemented so as to convert the regular expression into the postfix notation.
    '''
    exp = RegExpToString(exp)
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
    output2 = []
    op = []
    #all operators are left associative

    for i in exp:
        buffer = Node(i)
        if buffer.is_leaf:
            output2.append(buffer)
        else:
            if buffer.data == "(":
                op.append(buffer)
            elif buffer.data == ")":
                while op[-1].data != "(":
                    output2.append(op.pop())
                if op[-1].data == "(":
                    op.pop()
            else:
                while (op and check_precedence(buffer.data, op[-1].data)
                       and op[-1].data != '('):
                    output2.append(op.pop())
                op.append(buffer)
    while op:
        output2.append(op.pop())
#    for i in output2:
#        print(i)
    return output2


#Remember to add the "#" at the end of the input string


class TreeNode:
    def __init__(self, right, left, op):
        self.right = right
        self.left = left
        self.data = op

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data)
        if self.right:
            self.right.PrintTree()  #printing the tree


#Remember to add the "#" at the end of the input string
class SyntaxTree:
    '''This class is a data structure that keeps the regular expression as a Syntax Tree.
    '''
    def __init__(self, char):
        self.right = None
        self.left = None
        self.data = Node(char)

    def insert(self, char):
        self.root.data = "Delete this line pls"


#        if char.is_leaf:

#if self.data.is_leaf == true -> this is a leaf
#if self.data != "" and self.data.is_leaf -> give a unique number
#elif this is a node -> go left and go right
#LOOK BELOW:
#e.g. a(a|b)*b is aab|*b. is:
#.
#| \
#(or) b
#|\
#a *
#  |
#  b


def testing(sentence):
    postfix = RegExp2Postfix(sentence)
    stack = []
    for i in postfix:
        if not i.is_leaf:
            if len(stack):  #checking if stack is empty
                right = stack.pop()
            else:
                right = Node("")
            if len(stack):
                left = stack.pop()
            else:
                left = Node("")
            stack.append(TreeNode(right, left, i))
        else:
            stack.append(i)
    tree = stack.pop()
    tree.PrintTree()
