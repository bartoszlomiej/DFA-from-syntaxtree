COUNT = [10]  #global variable


class Node:
    '''
    The basic structure that keeps Node and Leaves
    '''
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
        '''To print the data in convenient way'''
        return self.data


def RegExpToString(exp):
    '''
    Converts the string to the another notation - the concatenation symbol will be the '.' so a make to easier in later conversion to the Postfix notation
    '''
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
    precedence = {'*': 2, '?': 2, '+': 2, '.': 1, '|': 0, '(': 3}
    #HERE WAS THE MAJOR CHANGE, INITIALLY IT WAS '<='
    if precedence[char] < precedence[top]:
        return True
    return False


def RegExp2Postfix(exp):
    '''
    Converts the regular expression to the postfix notation

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
    '''
    Is a simple object of the tree node. It stores the information about the node children as well as it stores its data (the class Node)
    '''
    def __init__(self, right, left, op, id):
        '''The basic constructor that takes 3 parameters: right - the right node, left - the left node, op - Node'''
        self.right = right
        self.left = left
        self.data = op
        self.nullable = False
        self.id = id
        self.prev_position = []
        self.last_prev_position = []
        self.follow_list = []

    def PrintTree(self):
        '''Prints the tree'''
        if self.left:
            self.left.PrintTree()
        print(self.data, self.nullable, self.id, self.prev_position,
              self.last_prev_position, self.follow_list)
        if self.right:
            self.right.PrintTree()  #printing the tree

    def my_nullable(self):
        '''
        checks if the language generate by the subtree contains the empty string ε
        '''
        if self.data.data == "|":
            if self.left:
                if self.left.my_nullable():
                    self.nullable = True
            if self.right:
                if self.right.my_nullable():
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
        if self.right:
            self.right.my_nullable()
            self.right.is_nullable()

    def first(self):
        '''
        Returns the set of positions current under node that can match the first symbol of a string
        '''
        if self.prev_position:  #blocks from repeating the code for the same node several times
            return self.prev_position
        if self.data.data == "|":  # return last(c1) or last(c2)
            if self.left:  #this iteration is being made so as not to have nested tables
                for i in self.left.first():
                    if not i in self.prev_position:
                        self.prev_position.append(i)
            if self.right:
                for i in self.right.first():
                    if not i in self.prev_position:
                        self.prev_position.append(i)
            return self.prev_position
        elif self.data.data == ".":
            if self.left:
                if self.left.nullable:  #if nullable(c1)
                    for i in self.left.first():
                        if not i in self.prev_position:
                            self.prev_position.append(i)
                    if self.right:
                        for i in self.right.first():
                            if not i in self.prev_position:  #protection from duplicates
                                self.prev_position.append(i)
                    return self.prev_position
                else:
                    return self.left.first()
        elif self.data.data == "?" or self.data.data == "*" or self.data.data == "+":
            if self.right:  #as the leaves are pushed to the right, then to the left
                return self.right.first()
        elif self.data.data == "":
            return self.prev_position
        else:
            self.prev_position.append(self.id)
            return self.prev_position

    def assign_first(self):
        '''
        Performes the first() for each node in the tree
        '''
        if self.left:
            self.left.assign_first()
        t = self.first()  #just for dbg
        self.prev_position = t
        if self.right:
            self.right.assign_first()  #printing the tree

    def last(self):
        '''
        Returns the set of positions under each node that can match the last symbol of a string
        '''
        if self.last_prev_position:  #blocks from repeating the code for the same node several times
            return self.last_prev_position
        if self.data.data == "|":  #return last(c1) or last(c2)
            if self.left:  #this iteration is being made so as not to have nested tables
                for i in self.left.last():
                    if not i in self.last_prev_position:
                        self.last_prev_position.append(i)
            if self.right:
                for i in self.right.last():
                    if not i in self.last_prev_position:
                        self.last_prev_position.append(i)
            return self.last_prev_position
        elif self.data.data == ".":
            if self.right:
                if self.right.nullable:  #if nullable(c2)
                    for i in self.right.last():
                        if not i in self.last_prev_position:
                            self.last_prev_position.append(i)
                    if self.left:
                        for i in self.left.last():
                            if not i in self.last_prev_position:
                                self.last_prev_position.append(i)
                    return self.last_prev_position  #return last(c1) or last(c2)
                else:
                    return self.right.last()  #return last(c2)
        elif self.data.data == "?" or self.data.data == "*" or self.data.data == "+":
            if self.right:
                return self.right.last()  #return last(c1)
        elif self.data.data == "":
            return self.last_prev_position
        else:
            self.last_prev_position.append(self.id)
            return self.last_prev_position

    def assign_last(self):
        '''
        Performs the first() for each node in the tree
        '''
        if self.left:
            self.left.assign_last()
        t = self.last()
        self.last_prev_position = t
        if self.right:
            self.right.assign_last()

    def find_leaf(self, id):
        '''
        Traverse the tree in order to find the given leaf.
        returns the object of class Node
        '''
        ret_val = None
        if self.left:  #for each node in the table do:
            ret_val = self.left.find_leaf(id)
            if ret_val:
                return ret_val
        if self.data.is_leaf and self.id == id:
            return self  #check if the id and leaf matches
        if self.right:
            ret_val = self.right.find_leaf(id)
            if ret_val:
                return ret_val
        return ret_val

    def update_follow(self, id, second_param):
        '''
        Traverse the tree in order to find the given leaf.
        returns the object of class Node
        '''
        if self.left:  #for each node in the table do:
            self.left.update_follow(id, second_param)

        if self.data.is_leaf and self.id == id:
            for i in second_param:  #it is in fact follow(i) = follow(i) + second_param()
                if not i in self.follow_list:  #so as not to store duplicates
                    self.follow_list.append(i)
        if self.right:
            self.right.update_follow(id, second_param)

    def follow(self):
        '''
        returns the set of positions that can follow the position n in the 
        syntax tree if and only if the leaf have the input symbol (it is non-empty)

        follow(i) - follow of the leaf of id i
        '''
        if self.data.data == ".":
            for i in self.left.last_prev_position:
                self.update_follow(i, self.right.prev_position)
        elif self.data.data == "*" or self.data.data == "+":
            for i in self.last_prev_position:
                self.update_follow(i, self.prev_position)

    def follow_for_each_node(self):
        '''
        Calculates the follow for each node
        '''
        if self.left:  #for each node in the table do:
            self.left.follow_for_each_node()
        self.follow()
        if self.right:
            self.right.follow_for_each_node()

    def print2DUtil(self, root, space):
        # Base case
        if (root == None):
            return
        space += COUNT[0]

        self.print2DUtil(root.right, space)
        print()
        for i in range(COUNT[0], space):
            print(end=" ")
        print(root.data)
        self.print2DUtil(root.left, space)

    def print2D(self):
        # space=[0]
        # Pass initial space count as 0
        self.print2DUtil(self, 0)


class SyntaxTree:
    '''
    This class is a data structure that keeps the regular expression as a Syntax Tree.
    '''
    def __init__(self):
        self.root = None

    def create(self, sentence):
        postfix = RegExp2Postfix(sentence)
        stack = []
        counter = 1
        for i in postfix:
            if not i.is_leaf:
                if stack:  #checking if stack is empty
                    right = stack.pop()
                else:
                    right = TreeNode(None, None, Node(""), None)
                if stack:
                    left = stack.pop()
                else:
                    left = TreeNode(None, None, Node(""), None)
                stack.append(TreeNode(right, left, i, None))
            else:
                stack.append(TreeNode(None, None, i, counter))
                counter = counter + 1
        #performing all necessary operation that makes the syntax tree finished
        self.root = stack.pop()
        self.root.is_nullable()
        self.root.assign_first()
        self.root.assign_last()
        self.root.follow_for_each_node()

    def PrintTree(self):
        '''
        Prints the tree starting from the root
        '''
        self.root.PrintTree()


class DFA:
    def __init__(self):
        '''
        Initialize the all variables in the DFA object

        Variables:
        Dstate - dictionary - key - set of positions , value - state spanned by those positions
        Dtran - dictionary - key - a pair (State, letter), value -  next state
        final_states - list - keeps all final states
        '''
        self.Dstate = {}
        self.Dtran = {}
        self.final_states = []

    def construct(self, tree, string):
        '''
        Constructs the DFA on the basis of the syntax tree and the given regular expression.

        The algorithm that is implemented can be seen in the final documentation.
        '''
        s0 = tree.root.prev_position
        self.Dstate[tuple(s0)] = 'unmarked'
        i = 0
        keys = list(self.Dstate.keys())  #list of tuples of keys
        prev_list = []  #keeps the follow from previous iterations
        while i < len(keys):
            if self.Dstate[keys[i]] == 'unmarked':
                self.Dstate[keys[i]] = chr(i + 65)
                for a in string:
                    j = 0
                    while j < len(keys) and keys[j] != 'unmarked':
                        prev_list.clear()
                        for l in keys[j]:
                            leaf = tree.root.find_leaf(l)
                            if not leaf:
                                print(
                                    "There is no such letter in the alphabeth")
                                break
                            if leaf.data.data == a.data:
                                if leaf.follow_list:
                                    prev_list = prev_list + leaf.follow_list  #glueing the follow
                                    if not tuple(prev_list) in self.Dstate:
                                        self.Dstate[tuple(
                                            prev_list)] = 'unmarked'
                                self.Dtran[(self.Dstate[keys[i]],
                                            a.data)] = tuple(prev_list)
                        j = j + 1
                keys = list(self.Dstate.keys())
            i = i + 1

        #Translation of final Dtrans to states
        for i in list(self.Dtran.keys()):
            if self.Dtran[i] in self.Dstate.keys():
                self.Dtran[i] = self.Dstate[self.Dtran[i]]

        #Appending the final states to the list
        for i in self.Dtran.keys():
            if not self.Dtran[i]:
                self.final_states.append(i[0])

    def printDFA(self):
        '''
        Prints the information about all states, transitions, and final states.
        '''
        print("States:")
        for i in self.Dstate.keys():
            print(i, self.Dstate[i])
        print("Transitions")
        for i in self.Dtran.keys():
            print(i, self.Dtran[i])
        print("Final state:")
        print(self.final_states)

    def check_string(self, sentence):
        '''
        Checks whether the given string is in the alphabeth created by constructed DFA
        '''
        state = 'A'  #it is always the initial state
        for i in sentence:
            if (state, i) in self.Dtran.keys():
                state = self.Dtran[(state, i)]
            else:
                return False  #if there is a transition to unknown state, then this string is not in this DFA
        if state in self.final_states:
            return True
        return False


def main(regex, sentence):
    tree = SyntaxTree()
    tree.create(regex)
    print("===Print tree===")
    print("a|null|id|first|last|follow")
    tree.PrintTree()
    print("===Print DFA===")
    dfa = DFA()
    postfix = RegExp2Postfix(
        regex
    )  #it is necessary, mostly to add # to the end - the final state indicator
    dfa.construct(tree, postfix)
    dfa.printDFA()
    print("===Checking the string===")
    print("Is '", sentence, "' in this DFA?")
    print(dfa.check_string(sentence))
    print("===Print Tree in graphical form===")
    tree.root.print2D()
    return dfa


def test1():
    dfa = main('(ab)+c', 'abababc')
    print("===Further tests===")
    print(dfa.check_string('abc'))
    print(dfa.check_string('abccccc'))
    print(dfa.check_string('ababc'))


def test2():
    dfa = main('abc((ab)|c)*', 'abcab')
    print("===Further tests===")
    print(dfa.check_string('abc'))
    print(dfa.check_string('abcc'))
    print(dfa.check_string('abcabcabab'))


def test3():
    dfa = main('(a|b)*abb', 'abbabb')
    print("===Further tests===")
    print(dfa.check_string('abb'))
    print(dfa.check_string('aabb'))


def test4():
    dfa = main('(ab)*(p|q)(p|q)*', 'abababpqpqpqpqpppqqqq')
    print("===Further tests===")
    print(dfa.check_string('p'))
    print(dfa.check_string('qpppp'))


def test5():
    dfa = main('a(a|b*|(c+))b', 'aab')
    print("===Further tests===")
    print(dfa.check_string('abbbbb'))
    print(dfa.check_string('ab'))


def test6():
    dfa = main('(a|b)*abb', 'abba')
    print("===Further tests===")
    print(dfa.check_string('abba'))
    print(dfa.check_string('ab'))


def test7():
    dfa = main('(ab)|c ', 'abcabc')
    print("===Further tests===")
    print(dfa.check_string('abc'))
    print(dfa.check_string('abab'))
