# -*- coding: utf-8 -*-

import operator

from pythonds.basic.stack import Stack
from pythonds.trees.binaryTree import BinaryTree

def func1( arg1 ):
    print( "rule ======", rule )
    return True

def func2( arg1 ):
    return False

def func3( arg1, arg2 ):
    return True

def func4( arg1, arg2, arg3, arg4 ):
    return False

def RuleParser( fpexp ):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    is_func_args = False
    for i in fplist:
        # Open bracket.
        if i == '(':
            if is_func_args:
                parent = pStack.pop()
                currentTree = parent
            currentTree.insertLeft('')
            pStack.push( currentTree )
            currentTree = currentTree.getLeftChild()
            is_func_args = False
        # Function name or arguments.
        elif i.lower() not in [ 'and', 'or', ')' ]:
            if not is_func_args:
                currentTree.setRootVal( (i, []) )
                #parent = pStack.pop()
                #currentTree = parent
                is_func_args = True
                continue
            currentTree.key[1].append( i )
        elif i.lower() in [ 'and', 'or' ]:
            if is_func_args:
                parent = pStack.pop()
                currentTree = parent
            currentTree.setRootVal( i )
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
            is_func_args = False
        elif i == ')':
            if is_func_args:
                parent = pStack.pop()
                currentTree = parent
            currentTree = pStack.pop()
            is_func_args = False
        else:
            raise ValueError
    return eTree

def printexp(tree):
    sVal = ""
    if tree:
        if tree.getLeftChild():
            sVal = printexp(tree.getLeftChild())
        sVal = sVal + str(tree.key[0] + " {}".format( " ".join( tree.key[1] ) ) if type(tree.key) is tuple else " {} ".format( tree.key ) )
        if tree.getLeftChild():
            sVal = sVal + printexp(tree.getRightChild())
        if tree.getLeftChild() and tree.getLeftChild():
            sVal = "( {} )".format( sVal )
    return sVal

def postordereval(tree):
    opers = { 'and' : operator.and_, 'or' : operator.or_ }
    res1 = None
    res2 = None
    if tree:
        res1 = postordereval( tree.getLeftChild() )
        res2 = postordereval( tree.getRightChild() )
        if res1 is not None and res2 is not None:
            if type( res1 ) is not bool:
                res1 = globals()[res1[0]]( *res1[1] )
            if type( res2 ) is not bool:
                res2 = globals()[res2[0]]( *res2[1] )
            return opers[ tree.getRootVal().lower() ]( res1, res2 )
        else:
            return tree.getRootVal()

if __name__ == "__main__":
    rules = [ "( func1 arg1 AND func1 arg1 )",
              "( ( func1 arg1 OR func2 arg2 ) AND ( func3 arg3 arg4 AND func4 arg1 arg2 arg3 arg4 ) )", \
              "( ( func1 arg1 AND func2 arg2 ) OR func3 arg1 arg2 )" ]
    # Check input rules are parsed correct.
    for rule in rules:
        root = RuleParser( rule )
        # Example string must match the serialized tree string.
        result = printexp( root )
        if result != rule:
            print( "AssertionError:\n  expected: [{}],\n  actual:   [{}]".format( rule, result ) )
    # 
    assert postordereval( root )
