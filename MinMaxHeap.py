# Kayla Seidel
# Big Homework- Min-Max Heap

# "I hereby certify that this program is solely the result of my own work and
# is in compliance with the Academic Integrity policy of the course syllabus
# and the academic integrity policy of the CS department.”

# A min-max heap is a "complete binary tree data structure which combines the
# usefulness of both a min-heap and a max-heap, that is, it provides constant
# time retrieval and logarithmic time removal of both the minimum and maximum
# elements in it" (Wikipedia). This min-max heap includes methods to insert
# into the heap, find the minimum node in the heap, find the maximum node,
# remove the minimum node, remove the maximum node, and check whether the heap
# is a fulfills the required properties to be considered a min-max heap.
# It also includes thorough pytests to test whether the program works.

import random
import math
import pytest

# Node class
class Node(object):
    def __init__(self, k, d): # Node constructor
        self.key  = k         # key of node
        self.data = d         # data of node

# MinMaxHeap class
class MinMaxHeap(object):
    def __init__(self, size):       # Min-Max Heap class constructor
        self.__arr = [None] * size  # heap is stored as an array
        self.__nElems = 0           # no items are initially in the array
    
    # get index of the left child of the current node
    def __leftChildIndex(self, cur): return (2*cur) + 1
    # get index of the parent of the current node
    def __parentIndex(self, cur): return (cur-1) // 2
    
    # If the heap is not full, inserts a node with inputed key and data at the
    # end of the heap and then calls trickleUp() on the newly inserted node to
    # rebalance and maintain the min-max heap properties.
    # Returns True if the insert was successful and False if the heap is
    # full and therefore the insert was unsuccessful.
    # Supports duplicate key/data pairs being added to the heap.
    def insert(self, k, d):
        # Fail if the heap is full
        if self.__nElems == len(self.__arr): return False
        
        # Place new node at end of heap & trickle it up
        self.__arr[self.__nElems] = Node(k, d)
        self.__trickleUp(self.__nElems)
        self.__nElems += 1  # add one to # of elements in heap
        return True         # return True if successfully added node to heap
    
    # Determines if the node at the index inputed is on a min-level.
    # Calculates what level the node is on and then checks whether it is an
    # even level (min) or an odd level (max).
    # Returns True if it is on a min-level and False if it is on a max-level.
    def __minLevel(self, cur):
        level = math.floor(math.log2(cur+1)) # find level of index
        
        # return True if on a min level, False if not
        return level % 2 == 0
    
    # Checks what level the inputed index's node is on and compares its key
    # with the key of it's parent.
    # Swaps the nodes if appropiate and then recursively trickles up into the
    # appropriate node
    def __trickleUp(self, cur):
        bottom = self.__arr[cur]        # the recently inserted Node
        parent = self.__parentIndex(cur)  # its parent's location
        
        # while cur hasn't reached the root
        if cur > 0:
            # if cur is on a min level
            if self.__minLevel(cur):
                # if the recently inserted key is greater than its parent key
                if bottom.key > self.__arr[parent].key:
                    temp = self.__arr[cur]                  # swap the 2
                    self.__arr[cur] = self.__arr[parent]
                    self.__arr[parent] = temp
                    
                    self.__trickleUpMax(parent) # recursively trickle up on max nodes
                else:
                    self.__trickleUpMin(cur) # recursively trickle up on min nodes
            
            # if cur is on a max level
            else:
                # if the recently inserted key is less than its parent key
                if bottom.key < self.__arr[parent].key:
                    temp = self.__arr[cur]                  # swap the 2
                    self.__arr[cur] = self.__arr[parent]
                    self.__arr[parent] = temp
                    
                    self.__trickleUpMin(parent) # recursively trickle up on min nodes
                else:
                    self.__trickleUpMax(cur) # recursively trickle up on max nodes
                    
    # Compares the inputed index's node with the nodes of it's ancestors
    # to make sure that its key is greater than min level nodes above it.
    # If not, swaps the 2 nodes and recursively checks the grandparent node.
    def __trickleUpMin(self, cur):
        # find index of parent and grandparent of current index
        parent = self.__parentIndex(cur)
        grandparent = (parent-1) // 2
        
        # if cur has a grandparent and cur's key is greater than grandparent's key
        if grandparent >= 0 and self.__arr[cur].key < self.__arr[grandparent].key:
            temp = self.__arr[cur]                      # swap the 2
            self.__arr[cur] = self.__arr[grandparent]
            self.__arr[grandparent] = temp
 
            self.__trickleUpMin(grandparent) # recursively trickle up on min nodes    
     
    # Compares the inputed index's node with the nodes of it's ancestors
    # to make sure that its key is less than the max level nodes above it.
    # If not, swaps of the 2 nodes and recursively checks the grandparent node.
    def __trickleUpMax(self, cur):
        parent = self.__parentIndex(cur)         # parent index
        grandparent = self.__parentIndex(parent) # grandparent index
        
        # if cur has a grandparent and cur's key is greater than grandparent's key
        if grandparent >= 0 and self.__arr[cur].key > self.__arr[grandparent].key:
            temp = self.__arr[cur]                      # swap the 2
            self.__arr[cur] = self.__arr[grandparent]
            self.__arr[grandparent] = temp
            
            self.__trickleUpMax(grandparent) # recursively trickle up on max nodes        
            
    # Finds the minimum node in the heap (node with smallest key) and returns
    # a tuple of its key/data.
    # The minimum key in the heap will be the root node's key.
    def findMinimum(self):
        # if heap is empty, return None
        if self.__nElems == 0: return None
        
        # if heap is not empty, return the root node's key/data
        return self.__arr[0].key, self.__arr[0].data
    
    # Finds the maximum node in the heap (node with largest key) and returns
    # a tuple of its key/data.
    # The maximum key in the heap will be the greater key of the root's left
    # child and right child.
    def findMaximum(self):
        # if heap is empty, return None
        if self.__nElems == 0: return None
        
        # if heap has 1 item, it is the max: return its key/data
        if self.__nElems == 1: return self.__arr[0].key, self.__arr[0].data
        
        # if heap has 2 items, second element is the max: return its key/data
        if self.__nElems == 2: return self.__arr[1].key, self.__arr[1].data
        
        # if more than 2 items in heap, whichever node's key on
        # level 1 (max level) is greater is the maximum key
        maximum = self.__arr[2]
        if self.__nElems > 2:
            if self.__arr[1].key > self.__arr[2].key:
                maximum = self.__arr[1]
        
        # return the maximum node's key and data
        return maximum.key, maximum.data
    
    # Removes the first element of the heap,whose key has the minimum value, 
    # and replaces it with the last element of the array.
    # Makes sure to garbage collect the last position.
    # Compares the node now in the root position of the heap in order to
    # maintain heap property throughout the heap, ensuring that
    # each node on the min levels are less than all of their descendants
    # Returns a tuple of the removed node's key and data.
    def removeMin(self):
        # if heap is empty, return None
        if self.__nElems == 0: return None

        # save the node from the root in order to return its key/data later
        root = self.__arr[0]
        self.__nElems -= 1  # decrement # of elements in array by 1
        
        # place the last Node in the heap into the root location
        self.__arr[0] = self.__arr[self.__nElems]
        self.__arr[self.__nElems] = None  # garbage collect
        # call trickle down on the root index to restore heap property
        self.__trickleDownMin(0)
        
        # return key/data of removed node
        return root.key, root.data
    
    # Removes the element in the heap whose key has the maximum value
    # and replaces it with the last element of the array, making sure to
    # garbage collect the last position.
    # Calls trickleDownMax() to compare the node now that has replaced
    # the removed node to maintain heap property throughout the heap, ensuring
    # that each node on the max levels are greater than all of their descendants.
    # Returns a tuple of the removed node's key and data.
    def removeMax(self):
        maximum = None  # max node
        maxInd = 0      # max index
        
        # if the heap is empty, return None
        if self.__nElems == 0: return None
        
        # if heap has 1 item, it is the max and its index is the max index
        if self.__nElems == 1:
            maxInd = 0
            maximum = self.__arr[0]
            
        # if heap has 2 items, 2nd element is the max and its index is the max index
        if self.__nElems == 2: 
            maxInd = 1
            maximum = self.__arr[1]
        
        # if more than 2 items in heap, whichever node's key on level 1 (max
        # level) is greater is the maximum key and its index is the max index
        if self.__nElems > 2:
            if self.__arr[1].key > self.__arr[2].key:
                maxInd = 1
                maximum = self.__arr[1]
            else:
                maxInd = 2
                maximum = self.__arr[2]
        
        self.__nElems -= 1 # decrement # of items in array by 1
        
        # place the last Node in the heap into the root location
        self.__arr[maxInd] = self.__arr[self.__nElems]
        self.__arr[self.__nElems] = None  # garbage collect
        # call trickle down on the max index to restore heap property
        self.__trickleDownMax(maxInd)
        
        # return key/data of removed node
        return maximum.key, maximum.data        
    
    # Takes the inputed index's node and returns a list of the node's children
    def __childrenOf(self, index):
        # find index of left and right child of given index
        leftChild  = self.__leftChildIndex(index)
        rightChild = leftChild + 1
        
        # create a list of children and add the left and right child indexes,
        # if they exist
        children = []
        if leftChild < self.__nElems: children += [leftChild]
        if rightChild < self.__nElems: children += [rightChild]
        
        return children # return the newly created list of indexes
        
    # Takes list of indexes of children of a given node from childrenOf(), finds
    # the indexes of each of those children (grandchildren), and creates a new
    # list of the indexes of all children and grandchildren of the given index.
    # Returns the new list of combined children and grandchildren.
    def __childrenAndGrandchildrenOf(self, index):
        children = self.__childrenOf(index)
        
        # for each index in the list
        for child in children:
            # find the index of left and right children of each index
            leftGrandchild  = self.__leftChildIndex(child)
            rightGrandchild = leftGrandchild + 1
            
            if leftGrandchild < self.__nElems:  # if there is a left child,
                children += [leftGrandchild]    # add the index to the list
            if rightGrandchild < self.__nElems: # if there is a right child,
                children += [rightGrandchild]   # add the index to the list
        
        # return combined list of children and grandchildren
        return children
    
    # Takes list of indexes of all children and grandchildren of given node
    # from childrenAndGrandchildrenOf() and returns the smallest index
    # from the list to get the smallest descendant.
    def __smallestDescendant(self, index):
        kids = self.__childrenAndGrandchildrenOf(index)
        
        smallest = kids[0]
        
        # for each index in the list, if the key of the node in that index in
        # the heap is smaller than the current smallest key, then that index
        # is the smallest
        for i in range(len(kids)):
            if self.__arr[kids[i]].key < self.__arr[smallest].key:
                smallest = kids[i]
                
        return smallest # return index of smallest descendant
    
    # Takes list of indexes of all children and grandchildren of given node
    # from childrenAndGrandchildrenOf() and returns the largest index
    # from the list to get the largest descendant.
    def __largestDescendant(self, index):
        kids = self.__childrenAndGrandchildrenOf(index)
        
        largest = kids[0]
        
        # for each index in the list, if the key of the node in that index in
        # the heap is larger than the current smallest key, then that index
        # is the largest        
        for i in range(len(kids)):
            if self.__arr[kids[i]].key > self.__arr[largest].key:
                largest = kids[i]
                
        return largest # return index of largest descendant
    
    # Makes sure the array maintains heap property throughout the heap.
    # Compares the inputed index's node with the nodes of it's descendants
    # to make sure that min level nodes have keys less than all of their
    # descendants.
    # If not, swaps the nodes.
    def __trickleDownMin(self, cur):
        leftChild = self.__leftChildIndex(cur)
        rightChild = leftChild + 1
        
        # while cur has at least one child
        if leftChild < self.__nElems or rightChild < self.__nElems:
            # find index of smallest descendant of cur
            m = self.__smallestDescendant(cur)
        
            # find index of the parent of smallest descendant
            parentM = self.__parentIndex(m)
            
            # if m is a grandchild of cur...
            if m > rightChild:
                # if smallest descendant's key is less than current key
                if self.__arr[m].key < self.__arr[cur].key:
                    temp = self.__arr[m]            # swap them
                    self.__arr[m] = self.__arr[cur]
                    self.__arr[cur] = temp
                    
                    # if m's key is greater than its parent's key
                    if self.__arr[m].key > self.__arr[parentM].key:
                        temp = self.__arr[m]        # swap them
                        self.__arr[m] = self.__arr[parentM]
                        self.__arr[parentM] = temp
                        
                    # recursively trickle down on min nodes
                    self.__trickleDownMin(m)
                    
            # if not a grandchild and smallest descendant's key is less than current key
            else:
                if self.__arr[m].key < self.__arr[cur].key:
                    temp = self.__arr[m]                # swap them
                    self.__arr[m] = self.__arr[cur]
                    self.__arr[cur] = temp
    
    # Makes sure the array maintains heap property throughout the heap.
    # compares the inputed index's node with the nodes of it's descendants
    # to make sure that max level nodes have keys greater than all of their
    # descendants.
    # If not, swaps the nodes.
    def __trickleDownMax(self, cur):
        leftChild = self.__leftChildIndex(cur)
        rightChild = leftChild + 1
        
        # while cur has at least one child
        if leftChild < self.__nElems or rightChild < self.__nElems:
            # find smallest descendant of cur
            m = self.__largestDescendant(cur)
        
            # find parent of smallest descendant
            parentM = (m-1) // 2        
            
            # if m is a grandchild
            if m > rightChild:
                # if largest descendant's key is greater than current key
                if self.__arr[m].key > self.__arr[cur].key:
                    temp = self.__arr[m]            # swap them
                    self.__arr[m] = self.__arr[cur]
                    self.__arr[cur] = temp
                    
                    # if m's key is less than its parent's key
                    if self.__arr[m].key < self.__arr[parentM].key:
                        temp = self.__arr[m]        # swap them
                        self.__arr[m] = self.__arr[parentM]
                        self.__arr[parentM] = temp
                    self.__trickleDownMax(m) # recursively trickle down on max nodes
            
            # if m is not a grandchild and largest descendant's key
            # is greater than current key
            else:
                if self.__arr[m].key > self.__arr[cur].key:
                    temp = self.__arr[m]                # swap them
                    self.__arr[m] = self.__arr[cur]
                    self.__arr[cur] = temp
    
    # Checks to make sure that the heap fulfills min-max heap properties
    # and is actually a min-max heap.
    # Goes through the nodes on each level, and recursively checks
    # to make sure that on a min level, all children have keys
    # greater than the current node's key, and on a max level, all children
    # have keys less than the current node's key.
    # If conditions are satisfied, returns True.
    # If not satisfied at any point in the heap, immediately returns False.
    # If the heap is empty or there is only one item in the heap, it is
    # definitely a min-max heap, so immediately returns True.
    def isMinMaxHeap(self, cur=0):
        # if the heap has none or one node, it is a heap
        if self.__nElems < 2: return True
        
        # find index of left and right children
        leftChild = self.__leftChildIndex(cur)
        rightChild = leftChild + 1
            
        # if it is a min level
        if self.__minLevel(cur):
            # if there is a left child, make sure it is not less than its
            # parent, and then recursively check the child's descendants
            if leftChild < self.__nElems:
                if self.__arr[leftChild].key < self.__arr[cur].key:
                    return False
                self.isMinMaxHeap(leftChild)
            
            # if there is a right child, make sure it is not less than its
            # parent, and then recursively check the child's descendants            
            if rightChild < self.__nElems:
                if self.__arr[rightChild].key < self.__arr[cur].key:
                    return False
                self.isMinMaxHeap(rightChild)
        
        # if its a max level
        elif not self.__minLevel(cur):
            # if there is a left child, make sure it is not greater than its
            # parent, and then recursively check the child's descendants            
            if leftChild < self.__nElems:
                if self.__arr[leftChild].key > self.__arr[cur].key:
                    return False
                self.isMinMaxHeap(leftChild)
            
            # if there is a right child, make sure it is not greater than its
            # parent, and then recursively check the child's descendants            
            if rightChild < self.__nElems:
                if self.__arr[rightChild].key > self.__arr[cur].key:
                    return False
                self.isMinMaxHeap(rightChild)
                
        # if made it through the heap and all nodes on min levels have keys less
        # than all of their descendants and all nodes on max levels have keys
        # greater than all of their descendants, return True
        return True
    
    # Returns node at inputed index
    def getItem(self, index):
        return self.__arr[index]

# Builds a min-max heap of inputed size and performs inserts into the heap.
# Checks to make sure that all inserted keys are actually in the heap.
# Returns a tuple of the heap and a sorted array of the inserted keys.
# >>in pytests, or client code, will need to isolate the 0th element of the
#    tuple to perform methods on the heap-- ex:
#         h = MinMaxHeap(size)
#         h[0].insert()
def makeHeap(size):
    h = MinMaxHeap(size)  # make a new heap with maximum # of elements
    
    arr = []           # make an array to add the keys inserted into the heap
    heapArray = []     # make another array to add heap's keys into afterwards
    sameKeys = True    # make variable to check if keys in heap are same as arr
    
    for i in range(size-1):  # insert items into heap
        key = random.randint(1, 100)
        data = chr(ord('A') + 1 + i)
        h.insert(key, data)             # add key, data to heap
        arr.append(key)
        
    for i in range(size-1):             # add keys in the heap to second array
        heapArray.append(h.getItem(i).key)
    
    for key in arr:                     # check that keys in arr are all
        if key not in heapArray:        # also in heapArray
            sameKeys = False
            
    assert sameKeys == True   # make sure inserted keys are still in heap  
    
    arr.sort()    # sort the array of keys
    
    return h, arr # return a tuple of the heap and the sorted array of keys

# test empty heap
def test_emptyHeap():
    h = MinMaxHeap(30)
    assert h.isMinMaxHeap() == True

# test heap with one node
def test_oneNodeHeap():
    h = MinMaxHeap(30)
    h.insert(43, "B")
    assert h.isMinMaxHeap() == True
    
# test inserts on a small heap
def test_insertSmallHeap():
    h = makeHeap(10)
    assert h[0].isMinMaxHeap() == True
    
# test inserts on a big heap
def test_insertBigHeap():
    h = makeHeap(10000)
    assert h[0].isMinMaxHeap() == True
    
# find the minimum node of an empty heap
def test_findMinEmptyHeap():
    h = MinMaxHeap(30)
    assert h.isMinMaxHeap() == True
    assert h.findMinimum() == None

# find the minimum node of a heap with one node
def test_findMinOneNode():
    h = MinMaxHeap(30)
    h.insert(43, "B")   
    
    assert h.isMinMaxHeap() == True
    assert h.findMinimum() == (43, "B")
    
# find the minimum node of a small heap
def test_findMinSmallHeap():
    h = makeHeap(10)
    
    h[0].insert(0, "G")
    assert h[0].findMinimum() == (0, "G")

# find the minimim node of a large heap
def test_findMinBigHeap():
    h = makeHeap(10000)
    
    h[0].insert(0, "G")
    assert h[0].findMinimum() == (0, "G")

# find the maximum node of an empty heap
def test_findMaxEmptyHeap():
    h = MinMaxHeap(30)
    assert h.isMinMaxHeap() == True
    assert h.findMaximum() == None
    
# find the maximum node of a heap with one node
def test_findMaxOneNode():
    h = MinMaxHeap(30)
    h.insert(43, "B")   
    
    assert h.isMinMaxHeap() == True
    assert h.findMaximum() == (43, "B")

# find the maximum node of a heap with 2 nodes
def test_findMaxTwoNodes():
    h = MinMaxHeap(30)
    h.insert(43, "B")
    h.insert(52, "O")
    
    assert h.isMinMaxHeap() == True
    assert h.findMaximum() == (52, "O")
    
    j = MinMaxHeap(30)
    j.insert(92, "G")
    j.insert(78, "K")
    
    assert j.isMinMaxHeap() == True
    assert j.findMaximum() == (92, "G")

# find the maximum node of a heap with 3 nodes
def test_findMaxThreeNodes():
    k = MinMaxHeap(30)
    k.insert(78, "K")
    k.insert(92, "G")
    k.insert(43, "B")
    
    assert k.isMinMaxHeap() == True
    assert k.findMaximum() == (92, "G")

# find the maximum node of a small heap
def test_findMaxSmallHeap():
    h = makeHeap(10)
    
    h[0].insert(101, "G")
    assert h[0].findMaximum() == (101, "G")

# find the maximum node of a large heap
def test_findMaxBigHeap():
    h = makeHeap(10000)
    
    h[0].insert(101, "G")
    assert h[0].findMaximum() == (101, "G")

# remove the minimum node of an empty heap
def test_removeMinEmptyHeap():
    h = MinMaxHeap(30)
    assert h.isMinMaxHeap() == True
    assert h.removeMin() == None
    assert h.isMinMaxHeap() == True

# remove the minimum node of a heap with one node
def test_removeMinOneNode():
    h = MinMaxHeap(30)
    h.insert(43, "B")   
    
    assert h.isMinMaxHeap() == True
    assert h.removeMin() == (43, "B")
    assert h.isMinMaxHeap() == True
    
# remove the maximum node of an empty heap
def test_removeMaxEmptyHeap():
    h = MinMaxHeap(30)
    assert h.isMinMaxHeap() == True
    assert h.removeMax() == None
    assert h.isMinMaxHeap() == True

# remove the maximum of a heap with one node
def test_removeMaxOneNode():
    h = MinMaxHeap(30)
    h.insert(43, "B")   
    
    assert h.isMinMaxHeap() == True
    assert h.removeMax() == (43, "B")
    assert h.isMinMaxHeap() == True
    
# remove the maximum node of a heap with 2 nodes
def test_removeMaxTwoNodes():
    h = MinMaxHeap(30)
    h.insert(43, "B")
    h.insert(52, "O")
    
    assert h.isMinMaxHeap() == True
    assert h.removeMax() == (52, "O")
    assert h.isMinMaxHeap() == True
    
    j = MinMaxHeap(30)
    j.insert(92, "G")
    j.insert(78, "K")
    
    assert j.isMinMaxHeap() == True
    assert j.removeMax() == (92, "G")
    assert j.isMinMaxHeap() == True

# remove the maximum node of a heap with 3 nodes
def test_removeMaxThreeNodes():
    k = MinMaxHeap(30)
    k.insert(78, "K")
    k.insert(92, "G")
    k.insert(43, "B")
    
    assert k.isMinMaxHeap() == True
    assert k.removeMax() == (92, "G")
    assert k.isMinMaxHeap() == True
    
# make removals of min and max from a small heap
def test_removeSmallHeap():
    h = makeHeap(10)
    
    h[0].removeMax()
    assert h[0].isMinMaxHeap() == True
    h[0].removeMin()
    assert h[0].isMinMaxHeap() == True
    h[0].removeMax()
    assert h[0].isMinMaxHeap() == True

# make removals of min and max from a large heap
def test_removeBigHeap():
    h = makeHeap(10000)
    
    h[0].removeMax()
    assert h[0].isMinMaxHeap() == True
    h[0].removeMin()
    assert h[0].isMinMaxHeap() == True
    h[0].removeMax()
    assert h[0].isMinMaxHeap() == True
    
# test inserts on a bunch of heaps
def test_tortureInsert():
    size = random.randint(1, 1000)
    for i in range(100):
        h = makeHeap(size)
        assert h[0].isMinMaxHeap() == True

# test a bunch of min and max removals on a bunch of heaps
def test_tortureRemove():
    size = random.randint(1, 1000)
    
    # loop for 100 times
    for i in range(100):
        # make randomly sized heap and assert its a min-max heap
        h = makeHeap(size)
        heap = h[0]
        arr = h[1]
        assert heap.isMinMaxHeap() == True
        
        # For half of the heap, do min removals, making sure the removed
        # node's key matches the key in each position of the sorted keys array.
        # Since the array is sorted, it is in ascending order of keys, so each
        # time a node is removed, its key should be in the next position of the list.
        for i in range(size//2):
            removed = heap.removeMin()
            assert removed[0] == arr[i]
        assert heap.isMinMaxHeap() == True
        
        # for the other half of the heap, do max removals, also making sure
        # the removed node's key matches the key in the next position of the 
        # sorted keys array
        for i in range((size//2) - 1):
            removed = heap.removeMax()
            assert removed[0] == arr[-i-1]
        assert heap.isMinMaxHeap() == True
    
    
pytest.main(["-v", "-s", "MinMaxHeap.py"])