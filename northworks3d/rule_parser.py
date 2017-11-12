# -*- coding: utf-8 -*-

import operator

from pythonds.basic.stack import Stack
from pythonds.trees.binaryTree import BinaryTree

def func1( arg1 ):
    print( "rule ======", rule )
    return True

def func2( arg1 ):
    return False

def func3( arg1 ):
    return True

def func4( arg1 ):
    return False

class RuleParser(object):
    tree = None
    operators = { 'and' : operator.and_, 'or' : operator.or_ }

    def __init__( self, rule, globals=globals() ):
        tokens = rule.split()
        pStack = Stack()
        self.tree = BinaryTree('')
        pStack.push( self.tree )
        current_tree = self.tree
        is_func_args = False
        self.globals = globals
        for token in tokens:
            # Open bracket.
            if token == '(':
                if is_func_args:
                    parent = pStack.pop()
                    current_tree = parent
                current_tree.insertLeft('')
                pStack.push( current_tree )
                current_tree = current_tree.getLeftChild()
                is_func_args = False
            # Function name or arguments.
            elif token.lower() not in [ 'and', 'or', ')' ]:
                if not is_func_args:
                    current_tree.setRootVal( (token, []) )
                    is_func_args = True
                    continue
                current_tree.key[1].append( token )
            elif token.lower() in [ 'and', 'or' ]:
                if is_func_args:
                    parent = pStack.pop()
                    current_tree = parent
                current_tree.setRootVal( token )
                current_tree.insertRight('')
                pStack.push(current_tree)
                current_tree = current_tree.getRightChild()
                is_func_args = False
            elif token == ')':
                if is_func_args:
                    parent = pStack.pop()
                    current_tree = parent
                current_tree = pStack.pop()
                is_func_args = False
            else:
                raise ValueError
        self.tree = current_tree
        # If we have only 1 node (Example: "func1 arg1"), then 
        # the root node is empty. Make it left child which is not empty.
        if self.tree.getRightChild() is None and self.tree.getLeftChild() is not None:
            self.tree = self.tree.getLeftChild()
    
    def eval_rule( self ):
        return self.eval_rule_( self.tree )
    
    def eval_rule_( self, tree ):
        left_child = None
        right_child = None
        if tree:
            left_child = self.eval_rule_( tree.getLeftChild() )
            right_child = self.eval_rule_( tree.getRightChild() )
            if left_child is not None and right_child is not None:
                return self.operators[ tree.getRootVal().lower() ]( left_child, right_child )
            else:
                root_value = tree.getRootVal()
                return self.globals[ root_value[0] ]( " ".join( root_value[1] ) ) if type( root_value ) is not bool else root_value
    
    def serialize( self ):
        return self.serialize_( self.tree )

    def serialize_( self, tree ):
        value = ""
        if tree:
            if tree.getLeftChild():
                value = self.serialize_( tree.getLeftChild() )
            current_node_value = "{} {}".format( tree.key[0], " ".join( tree.key[1] ) ) if type(tree.key) is tuple else " {}".format( tree.key )
            value += current_node_value
            if tree.getLeftChild():
                value = "{} {}".format( value, self.serialize_( tree.getRightChild() ) )
            if tree.getLeftChild() and tree.getLeftChild():
                value = "( {} )".format( value )
        return value

if __name__ == "__main__":
    rules = [ "( func1 arg1 AND func1 arg1 )",
              "( ( func1 arg1 OR func2 arg2 ) AND ( func3 arg3 arg4 AND func4 arg1 arg2 arg3 arg4 ) )", \
              "( ( func1 arg1 AND func2 arg2 ) OR func3 arg1 arg2 )",\
              "func1 arg1" ]
    # Check input rules are parsed correct.
    for rule in rules:
        tree = RuleParser( rule )
        # Example string must match the serialized tree string.
        result = tree.serialize()
        if result != rule:
            print( "AssertionError:\n  expected: [{}],\n  actual:   [{}]".format( rule, result ) )
    
    assert tree.eval_rule( )
