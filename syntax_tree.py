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

    def __str__(self):
        '''To print the data i convenient way'''
        return self.data


def RegExpToString(exp):
    '''Converts the string to the another notation - the concatenation symbol will be the '.' so a make to easier in later conversion to the Postfix notation'''
    op = ["*", "|", "+", "?", ")"]
    output = []
    counter = 0
    for i in exp:
        marker = False
        for o in op:
            if o == i:
                if output:
                    if output[-1] == ".":
                        output.pop()
        if i == "|":
            marker = True
        elif i == "(":
            marker = True
        output.append(i)
        if not marker:
            output.append(".")
    if output[-1] != ".":
        output.append(".")
    output.append("#")  #adding special symbol to indicate important states
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
    return output2


class TreeNode:
    '''Is a simple object of the tree node. It stores the information about the node children as well as it stores its data (the class Node)'''
    def __init__(self, right, left, op):
        '''The basic constructor that takes 3 parameters: right - the right node, left - the left node, op - Node'''
        self.right = right
        self.left = left
        self.data = op
        self.nullable = False
        self.id = 0
        self.prev_position = []

    def PrintTree(self):
        '''Prints the tree'''
        if self.left:
            self.left.PrintTree()
        print(self.data)
        if self.right:
            self.right.PrintTree()  #printing the tree

    def my_nullable(self):
        '''Check nullable for current node'''
        if self.data.data == "|":
            if self.left:
                if self.left.my_nullable():
                    self.nullable = True
            if self.right:
                if self.right.my_nullable():  #printing the tree
                    self.nullable = True
        elif self.data.data == ".":
            if self.left and self.right:
                if self.left.my_nullable() and self.right.my_nullable():
                    self.nullable = True
        elif self.data.data == "?" or self.data.data == "*":
            self.nullable = True
        elif self.data.data == "":
            self.nullable = True

    def is_nullable(self):
        '''Calculating nullable for each node and leaf'''
        if self.left:
            self.left.my_nullable()
            self.left.is_nullable()
        print(self.data, self.nullable)
        if self.right:
            self.right.my_nullable()
            self.right.is_nullable()

    def give_id(self, i):
        '''Each node has its unique identifier in the tree'''
        if self.left:
            self.id = self.left.give_id(self.id)
        if self.right:
            self.id = self.right.give_id(self.id)
        if self.data.is_leaf:
            if self.data.data != "":
                self.id = i + 1
        return self.id

        #    def first(self):
        '''calculate first for current node'''
        '''
        if self.data.data == "|":
            if self.left:
                if self.left.first():
                    return True
            if self.right:
                if self.right.first():  #printing the tree
                    return True
        elif self.data.data == ".":
            if self.left:
                if self.left.nullable:
                    if self.left.first():
                        return True
                    elif self.right:
                        if self.right.first():
                            return True
                else:
                    if self.left.first():
                        return True
        elif self.data.data == "?" or self.data.data == "*":
            if self.right:  #as the leaves are pushed to the right, then to the left
                if self.right.first():
                    return True
        elif self.data.data == "":
            if self.right.first():
                return Node("")
        return False
'''


class SyntaxTree:
    '''This class is a data structure that keeps the regular expression as a Syntax Tree.
    '''
    def __init__(self):
        self.root = None

    def create(self, sentence):
        postfix = RegExp2Postfix(sentence)
        stack = []
        for i in postfix:
            if not i.is_leaf:
                if len(stack):  #checking if stack is empty
                    right = stack.pop()
                else:
                    right = TreeNode(None, None, Node(""))
                if len(stack):
                    left = stack.pop()
                else:
                    left = TreeNode(None, None, Node(""))
                stack.append(TreeNode(right, left, i))
            else:
                stack.append(TreeNode(None, None, i))

        self.root = stack.pop()

    def PrintTree(self):
        self.root.PrintTree()

    def check_nullable(self):
        self.root.is_nullable()

    def give_id(self):
        self.root.give_id(0)


def main(sentence):
    tree = SyntaxTree()
    tree.create(sentence)
    print("===Tree===")
    tree.give_id()
    tree.PrintTree()
    print("===Nullable===")
    tree.check_nullable()
