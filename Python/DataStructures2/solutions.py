# solutions.py
"""Volume II Lab 5: Data Structures II (Trees). Solutions file."""

from matplotlib import pyplot as plt
from numpy.random import choice
from time import time


class SinglyLinkedListNode(object):
    """Simple singly-linked list node."""
    def __init__(self, data):
        self.value, self.next = data, None

class SinglyLinkedList(object):
    """A very simple singly-linked list with a head and a tail."""
    def __init__(self):
        self.head, self.tail = None, None
    def append(self, data):
        """Add a Node containing 'data' to the end of the list."""
        n = SinglyLinkedListNode(data)
        if self.head is None:
            self.head, self.tail = n, n
        else:
            self.tail.next = n
            self.tail = n

def iterative_search(linkedlist, data):
    """Find the node containing 'data' using an iterative approach.
    If there is no such node in the list, or if the list is empty,
    raise a ValueError.
    
    Inputs:
        linkedlist (LinkedList): a linked list object
        data: the data to find in the list.
    
    Returns:
        The node in 'linkedlist' containing 'data'.
    """
    current = linkedlist.head
    while current is not None:
        if current.value == data:
            return current
        current = current.next
    raise ValueError(str(data) + " is not in the list.")

# Problem 1: rewrite iterative_search() using recursion.
def recursive_search(linkedlist, data):
    """Find the node containing 'data' using a recursive approach.
    If there is no such node in the list, or if the list is empty,
    raise a ValueError.
    
    Inputs:
        linkedlist (LinkedList): a linked list object.
        data: the data to find in the list.
    
    Returns:
        The node in 'linkedlist' containing 'data'.
    """
    def _step(current):
        """Check the current node, and step right if not found."""
        if current is None:         # Base case 1: dead end
            raise ValueError(str(data) + " is not in the list.")
        if current.value == data:   # Base case 2: the data matches
            return current
        else:                       # Recurse if not found
            return _step(current.next)
    
    return _step(linkedlist.head)


class BSTNode(object):
    """A Node class for Binary Search Trees. Contains some data, a
    reference to the parent node, and references to two child nodes.
    """
    def __init__(self, data):
        """Construct a new node and set the data attribute. The other
        attributes will be set when the node is added to a tree.
        """
        self.value = data
        self.prev = None        # A reference to this node's parent node.
        self.left = None        # self.left.value < self.value
        self.right = None       # self.value < self.right.value
    

# Modify this class for problems 2 and 3
class BST(object):
    """Binary Search Tree data structure class.
    The 'root' attribute references the first node in the tree.
    """
    def __init__(self):
        """Initialize the root attribute."""
        self.root = None
    
    def find(self, data):
        """Return the node containing 'data'. If there is no such node in the
        tree, or if the tree is empty, raise a ValueError."
        """
        # First, check to see if the tree is empty
        if self.root is None:
            raise ValueError(str(data) + " is not in the tree.")
        
        # Define a recursive function to traverse the tree
        def _step(current, item):
            """Recursively step through the tree until the node containing
            'item' is found. If there is no such node, raise a Value Error.
            """
            if current is None:                     # Base case 1: dead end
                raise ValueError(str(data) + " is not in the tree.")
            if item == current.value:               # Base case 2: data matches
                return current
            if item < current.value:                # Step to the left
                return _step(current.left,item)
            else:                                   # Step to the right
                return _step(current.right,item)
        
        # Start the recursion on the root of the tree.
        return _step(self.root, data)
    
    # Problem 2: Implement BST.insert()
    def insert(self, data):
        """Insert a new node containing 'data' at the appropriate location.
        Do not allow for duplicates in the tree: if there is already a node
        containing 'data' in the tree, raise a ValueError.
        
        Example:
            >>> b = BST()       |   >>> b.insert(1)     |       (4)
            >>> b.insert(4)     |   >>> print(b)        |       / \
            >>> b.insert(3)     |   [4]                 |     (3) (6)
            >>> b.insert(6)     |   [3, 6]              |     /   / \
            >>> b.insert(5)     |   [1, 5, 7]           |   (1) (5) (7)
            >>> b.insert(7)     |   [8]                 |             \
            >>> b.insert(8)     |                       |             (8)
        """
        
        def _find_parent(current, item):
            """Recursively descend through the tree to find the node that
            should be the parent of the new node. Do not allow for duplicates.
            """
            assert current is not None              # Base case: failure
            if item == current.value:               # Base case: duplicate
                raise ValueError(str(item) + " is already in the tree.")
            elif item < current.value:              # Step to the left
                if current.left:
                    return _find_parent(current.left, item)
                else:                               # Base case: parent found
                    return current
            else:                                   # Step to the right
                if current.right:
                    return _find_parent(current.right, item)
                else:                               # Base case: parent found
                    return current
        
        n = BSTNode(data)                           # Make a new node
        if self.root is None:                       # Case 1: empty tree
            self.root = n                               # reset the root
        else:                                       # Case 2: use _find_parent
            parent = _find_parent(self.root,data)       # Get the parent
            if data < parent.value:                     # Insert as left child
                parent.left = n
            else:                                       # Insert as right child
                parent.right = n
            n.prev = parent                             # Double link
    
    # Problem 3: Implement BST.remove()
    def remove(self, data):
        """Remove the node containing 'data'. Consider several cases:
            - The tree is empty
            - The target is the root:
                - The root is a leaf node, hence the only node in the tree
                - The root has one child
                - The root has two children
            - The target is not the root:
                - The target is a leaf node
                - The target has one child
                - The target has two children
            If the tree is empty, or if there is no node containing 'data',
            raise a ValueError.
        
        Examples:
        
            >>> print(b)        |   >>> b.remove(1)     |   [3]
            [4]                 |   >>> b.remove(7)     |   [5]
            [3, 6]              |   >>> b.remove(6)     |   [8]
            [1, 5, 7]           |   >>> b.remove(4)     |
            [8]                 |   >>> print(b)        |
        """
        
        def _successor(node):
            """Find the next-largest node in the tree by travelling
            right once, then left as far as possible.
            """
            assert node.right is not None   # Function called inappropriately
            node = node.right               # Step right once
            while node.left:
                node = node.left            # Step left until done
            return node
        
        # Case 1: the tree is empty
        if self.root is None:
            raise ValueError("The tree is empty.")
        # Case 2: the target is the root
        target = self.find(data)
        if target == self.root:
            # Case 2a: no children
            if not self.root.left and not self.root.right:
                self.__init__()
            # Case 2b: one child
            if not target.right:
                self.root = target.left
            elif not target.left:
                self.root = target.right
            # Case 2c: two children
            else:
                pred = _successor(target)
                self.remove(pred.value)
                target.value = pred.value
            # reset the new root's prev to None
            if self.root:
                self.root.prev = None
        # Case 3: the target is not the root
        else:
            # Case 3a: no children
            if not target.left and not target.right:
                parent = target.prev
                if target.value < parent.value:
                    parent.left = None
                elif target.value > parent.value:
                    parent.right = None
            # Case 3b: one child
            elif not target.right:
                parent = target.prev
                if parent.right is target:
                    parent.right = target.left
                elif parent.left is target:
                    parent.left = target.left
                target.left.prev = parent
            elif not target.left:
                parent = target.prev
                if parent.right is target:
                    parent.right = target.right
                elif parent.left is target:
                    parent.left = target.right
                target.right.prev = parent
            # Case 3c: two children
            else:
                pred = _successor(target)
                self.remove(pred.value)
                target.value = pred.value
    
    def __str__(self):
        """String representation: a hierarchical view of the BST.
        Do not modify this method, but use it often to test this class.
        (this method uses a depth-first search; can you explain how?)
        
        Example:  (3)
                  / \     '[3]          The nodes of the BST are printed out
                (2) (5)    [2, 5]       by depth levels. The edges and empty
                /   / \    [1, 4, 6]'   nodes are not printed.
              (1) (4) (6)
        """
        
        if self.root is None:                   # Print an empty tree
            return "[]"
        # If the tree is nonempty, create a list of lists.
        # Each inner list represents a depth level in the tree.
        str_tree = [list() for i in xrange(_height(self.root) + 1)]
        visited = set()                         # Track visited nodes
        
        def _visit(current, depth):
            """Add the data contained in 'current' to its proper depth level
            list and mark as visited. Continue recusively until all nodes have
            been visited.
            """
            str_tree[depth].append(current.value)
            visited.add(current)
            if current.left and current.left not in visited:
                _visit(current.left, depth+1)  # travel left recursively (DFS)
            if current.right and current.right not in visited:
                _visit(current.right, depth+1) # travel right recursively (DFS)
        
        _visit(self.root, 0)                    # Load the list of lists.
        out = ""                                # Build the final string.
        for level in str_tree:
            if level != list():                 # Ignore empty levels.
                out += str(level) + "\n"
            else:
                break
        return out

class AVL(BST):
    """AVL Binary Search Tree data structure class. Inherits from the BST
    class. Includes methods for rebalancing upon insertion. If your
    BST.insert() method works correctly, this class will work correctly.
    Do not modify.
    """
    def _checkBalance(self, n):
        return abs(_height(n.left) - _height(n.right)) >= 2
    
    def _rotateLeftLeft(self, n):
        temp = n.left
        n.left = temp.right
        if temp.right:
            temp.right.prev = n
        temp.right = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n == self.root:
            self.root = temp
        return temp
    
    def _rotateRightRight(self, n):
        temp = n.right
        n.right = temp.left
        if temp.left:
            temp.left.prev = n
        temp.left = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n == self.root:
            self.root = temp
        return temp
    
    def _rotateLeftRight(self, n):
        temp1 = n.left
        temp2 = temp1.right
        temp1.right = temp2.left
        if temp2.left:
            temp2.left.prev = temp1
        temp2.prev = n
        temp2.left = temp1
        temp1.prev = temp2
        n.left = temp2
        return self._rotateLeftLeft(n)
    
    def _rotateRightLeft(self, n):
        temp1 = n.right
        temp2 = temp1.left
        temp1.left = temp2.right
        if temp2.right:
            temp2.right.prev = temp1
        temp2.prev = n
        temp2.right = temp1
        temp1.prev = temp2
        n.right = temp2
        return self._rotateRightRight(n)
    
    def _rebalance(self,n):
        """Rebalance the subtree starting at the node 'n'."""
        if self._checkBalance(n):
            if _height(n.left) > _height(n.right):
                # Left Left case
                if _height(n.left.left) > _height(n.left.right):
                    n = self._rotateLeftLeft(n)
                # Left Right case
                else:
                    n = self._rotateLeftRight(n)
            else:
                # Right Right case
                if _height(n.right.right) > _height(n.right.left):
                    n = self._rotateRightRight(n)
                # Right Left case
                else:
                    n = self._rotateRightLeft(n)
        return n
    
    def insert(self, data):
        """Insert a node containing 'data' into the tree, then rebalance."""
        # insert the data like usual
        BST.insert(self, data)
        # rebalance from the bottom up
        n = self.find(data)
        while n:
            n = self._rebalance(n)
            n = n.prev
    
    def remove(*args, **kwargs):
        """Disable remove() to keep the tree in balance."""
        raise NotImplementedError("remove() has been disabled for this class.")

def _height(current):
    """Calculate the height of a given node by descending recursively until
    there are no further child nodes. Return the number of children in the
    longest chain down. Helper function for the AVL class and BST.__str__.
    Do not modify.
                                node | height
    Example:  (c)                  a | 0
              / \                  b | 1
            (b) (f)                c | 3
            /   / \                d | 1
          (a) (d) (g)              e | 0
                \                  f | 2
                (e)                g | 0
    """
    if current is None:     # Base case: the end of a branch.
        return -1           # Otherwise, descend down both branches.
    return 1 + max(_height(current.right), _height(current.left))

from sys import stdout

# Problem 4: Test build and search speeds for LinkedList, BST, and AVL objects.
def plot_times(filename="English.txt", start=500, stop=5500, step=500):
    """Reach each line from the given file. This will be the data set.
    Vary n from 'start' to 'stop', incrementing by 'step'. At each
    iteration, take the first n words from the specified file.
    
    Time (separately) how long it takes to load a SinglyLinkedList, a BST, and
    an AVL with the data set of n items.
    
    Choose 5 random items from the data set. Time (separately) how long it
    takes to find all 5 items in each object.
    
    Create one plot with two lin-log subplots (use plt.semilogy() instead of
    plt.plot()). In the first subplot, plot the number of items in each
    dataset against the build time for each object. In the second subplot,
    plot the number of items against the search time for each object.
    
    Inputs:
        filename (str): the file to use in creating the data sets.
    
    Returns:
        Show the plot, but do not return any values.
    """
    
    # Initialize lists to hold results
    lls_build, lls_search = [], []
    bst_build, bst_search = [], []
    avl_build, avl_search = [], []

    with open(filename, 'r') as f:
        data = f.readlines()
    
    # Get the values [start, start + step, ..., stop - step]
    domain = []
    for n in xrange(start,stop,step):

        print "\rn =", n,; stdout.flush()
    
        # Initialize wordlist and data structures
        word_list = data[:n]
        bst = BST()
        avl = AVL()
        lls = SinglyLinkedList()
        
        # Time the singly-linked list build
        start = time()
        for word in word_list:
            lls.append(word)
        lls_build.append(time() - start)
        
        # Time the binary search tree build
        start = time()
        for word in word_list:
            bst.insert(word)
        bst_build.append(time() - start)
        
        # Time the AVL tree build
        start = time()
        for word in word_list:
            avl.insert(word)
        avl_build.append(time() - start)
        

        subset = choice(word_list, size=5, replace=False)
        # Time the singly-linked list search

        start = time()
        for target in subset:
            iterative_search(lls, target)
        lls_search.append(time() - start)

        start = time()
        for target in subset:
            bst.find(target)
        bst_search.append(time() - start)

        start = time()
        for target in subset:
            avl.find(target)
        avl_search.append(time() - start)


        # # Search Times
        # search1, search2, search3 = [], [], []
        # for i in xrange(5):
        #     target = word_list[randint(0, n-1)]
            
        #     # Time LinkedList.find
        #     start = time()
        #     iterative_search(lls, target)
        #     search1.append(time() - start)
            
        #     # Time BST.find
        #     start = time()
        #     bst.find(target)
        #     search2.append(time() - start)
            
        #     # Time AVL.find
        #     start = time()
        #     avl.find(target)
        #     search3.append(time() - start)
        
        # lls_search.append(sum(search1)/len(search1))
        # bst_search.append(sum(search2)/len(search2))
        # avl_search.append(sum(search3)/len(search3))
        domain.append(n)
    
    # Plot the data
    plt.subplot(121)
    plt.title("Build Times")
    plt.semilogy(domain,lls_build,label='Singly-Linked List')
    plt.semilogy(domain,bst_build,label='Binary Search Tree')
    plt.semilogy(domain,avl_build,label='AVL Tree')
    plt.ylabel("seconds")
    plt.xlabel("data points")
    plt.legend(loc='upper left')
    
    plt.subplot(122)
    plt.title("Search Times")
    plt.semilogy(domain,lls_search,label='Singly-Linked List')
    plt.semilogy(domain,bst_search,label='Binary Search Tree')
    plt.semilogy(domain,avl_search,label='AVL Tree')
    plt.ylabel("seconds")
    plt.xlabel("data points")
    plt.legend(loc='upper left')
    
    plt.show()


''' Garbage
# Use this function in problem 6 to implement sort_words().
def create_word_list(filename):
    """Read in a list of words from the specified file.
    Randomize the ordering and return the list.
    """
    myfile = open(filename, 'r')    # Open the file with read-only access
    content = myfile.read()         # Read in the text from the file
    lines = content.split('\n')     # Get each word, separated by '\n'
    lines = lines[:-1]              # Remove the last endline
                                    # Randomize, convert to a list, and return.
    return list(np.random.permutation(lines))
'''

# ============================= END OF SOLUTIONS ============================ #

import inspect

def test(student_module):
    """Test script. You must import the student's 'solutions.py' as a module.
    
     5 points for problem 1
    15 points for problem 2
    30 points for problem 3
    10 points for problem 4
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 80.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # Constructor
    def __init__(self):
        self.feedback = ""

    # Main routine
    def test_all(self, student_module):
        self.feedback = ""
        score = 0

        try:    # Problem 1: 5 points
            self.feedback += "\n\nProblem 1 (5 points):"
            points = self.problem1(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 2: 15 points
            self.feedback += "\n\nProblem 2 (15 points):"
            points = self.problem2(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 3: 30 points
            self.feedback += "\n\nProblem 3 (30 points):"
            points = self.problem3(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 4: 10 points
            self.feedback += "\n\nProblem 4 (10 points):"
            points = self.problem4(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message

        # Report final score.
        total = 60
        percentage = (100.0 * score) / total
        self.feedback += "\n\nTotal score: " + str(score) + "/"
        self.feedback += str(total) + " = " + str(percentage) + "%"
        if   percentage >=  98.0: self.feedback += "\n\nExcellent!"
        elif percentage >=  90.0: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print self.feedback
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t' + comments
        self.score = score

    # Helper Function
    def strTest(self, x, y, message):
        """Test to see if x and y have the same string representation."""
        if str(x) == str(y):
            return 1
        else:
            self.feedback += message
            self.feedback += "\nCorrect response:\n" + str(x)
            self.feedback += "\nStudent response:\n" + str(y)
            return 0

    # Problems
    def problem1(self, s):
        """Test recursive_search(). 5 points."""

        points = 0

        lls = LinkedList()
        # Check recursive_search on empty list (1 point)
        try:
            s.recursive_search(lls, 1)
            self.feedback += "\n\trecursive_search() failed on empty list"
        except ValueError:
            points += 1

        # Check recursive_search for items in list (3 points)
        lls.add(1)
        lls.add('a')
        lls.add(2)
        points += self.strTest(iterative_search(lls,1),
                               s.recursive_search(lls, 1),
                               "\n\trecursive_search(x) failed for x in list")
        points += self.strTest(iterative_search(lls, 'a'),
                               s.recursive_search(lls, 'a'),
                               "\n\trecursive_search(x) failed for x in list")
        points += self.strTest(iterative_search(lls, 2),
                               s.recursive_search(lls, 2),
                               "\n\trecursive_search(x) failed for x in list")

        # Check recursive_search for items not in list (1 point)
        try:
            s.recursive_search(lls, 3)
            self.feedback += "\n\trecursive_search(x) failed for x not in list"
        except ValueError:
            points += 1

        # Check that recursion is used somewhere
        text = inspect.getsourcelines(s.recursive_search)[0]; code = ""
        text = text[len(s.recursive_search.__doc__.splitlines()) + 1 :]
        for line in text: code += line
        print "\nStudent Code (check for recursion):\n", code
        credit = -1
        while credit > 1 or credit < 0:
            try:
                credit = int(input("\nScore out of 1: "))
            except:
                credit = -1
        if credit != 1:
            self.feedback += "\n\trecursive_search() must use recursion!"
        points *= credit

        return points

    def problem2(self, s):
        """Test BST.insert(). 15 Points."""

        points = 0

        # Empty tree (0 pts)
        tree1, tree2 = BST(), s.BST()
        self.strTest(tree1, tree2, "\n\tBST() failed initially!")

        # Inserting root (2 pts)
        tree1.insert(4); tree2.insert(4)
        points += 2*self.strTest(tree1, tree2, "\n\tBST.insert(4) failed "
                                 "on root insertion.\nPrevious tree:\n[]")

        def test_insert(value, solTree, stuTree):
            oldTree = str(solTree)
            solTree.insert(value); stuTree.insert(value)
            p = self.strTest(tree1, tree2, "\n\tBST.insert(" + str(value)
                            + ") failed.\nPrevious tree:\n" + oldTree)
            return p, solTree, stuTree

        # Inserting nonroot (9 pts)
        p, tree1, tree2 = test_insert( 2, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 1, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 3, tree1, tree2); points += p
        p, tree1, tree2 = test_insert(10, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 5, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 6, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 9, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 7, tree1, tree2); points += p
        p, tree1, tree2 = test_insert(11, tree1, tree2); points += p

        # Inserting already existing value (4 pts)
        def test_duplicate(value, stuTree):
            try:
                stuTree.insert(value)
                self.feedback += "\n\tBST.insert(" + str(value) + ") failed "
                self.feedback += "for " + str(value) + " already in tree"
                return 0
            except ValueError:
                return 1

        points +=   test_duplicate(4, tree2)
        points +=   test_duplicate(1, tree2)
        points += 2*test_duplicate(7, tree2)
        
        if points < 11:
            self.feedback += "\n\tAll BST.remove() tests are likely to fail"
            self.feedback += "\n\tunless all BST.insert() tests pass!"
        return points

    def problem3(self, s):
        """Test BST.remove(). 30 points."""

        points = 0

        def load_trees():
            solutions_tree, student_tree = BST(), s.BST()
            solutions_tree.insert( 4); student_tree.insert( 4)
            solutions_tree.insert( 2); student_tree.insert( 2)
            solutions_tree.insert( 1); student_tree.insert( 1)
            solutions_tree.insert( 3); student_tree.insert( 3)
            solutions_tree.insert(10); student_tree.insert(10)
            solutions_tree.insert( 5); student_tree.insert( 5)
            solutions_tree.insert( 6); student_tree.insert( 6)
            solutions_tree.insert( 9); student_tree.insert( 9)
            solutions_tree.insert( 7); student_tree.insert( 7)
            solutions_tree.insert(11); student_tree.insert(11)
            solutions_tree.insert(15); student_tree.insert(15)
            solutions_tree.insert(14); student_tree.insert(14)
            solutions_tree.insert(16); student_tree.insert(16)
            solutions_tree.insert(12); student_tree.insert(12)
            if str(solutions_tree) != str(student_tree):
                raise NotImplementedError("BST.remove() cannot be tested "
                                          "until BST.insert() is correct.")
            return solutions_tree, student_tree

        def test_remove(value, solTree, stuTree):
            oldTree = str(solTree)
            try:
                solTree.remove(value); stuTree.remove(value)
                p = self.strTest(tree1, tree2, "\n\tBST.remove(" + str(value)
                            + ") failed.\nPrevious tree:\n" + oldTree)
            except Exception as e:
                self.feedback += "\n\tError while removing " + str(value)
                self.feedback += ": " + str(e) + "\nPrevious tree:\n" + oldTree
                p = 0
            finally:
                return p, solTree, stuTree

        tree2 = s.BST()

        # Remove from empty tree (1 points)
        try:
            tree2.remove(5)
            self.feedback += "\n\tBST.remove() failed for empty tree"
        except ValueError:
            points += 1

        # Remove leaf (5 points)
        tree1, tree2 = load_trees()
        p, tree1, tree2 = test_remove( 1, tree1, tree2); points += p
        p, tree1, tree2 = test_remove( 7, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(12, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(16, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(14, tree1, tree2); points += p
        
        # Remove non-root with 1 child (5 points)
        tree1, tree2 = load_trees()
        p, tree1, tree2 = test_remove( 9, tree1, tree2); points += p
        p, tree1, tree2 = test_remove( 6, tree1, tree2); points += p
        p, tree1, tree2 = test_remove( 5, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(11, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(14, tree1, tree2); points += p

        # Remove non-root with 2 children (5 points)
        tree1, tree2 = load_trees()
        p, tree1, tree2 = test_remove( 2, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(15, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(10, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(11, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(12, tree1, tree2); points += p
        
        # Remove root with no children (2 point)
        tree1, tree2 = BST(), s.BST()
        tree1.insert(10); tree2.insert(10)
        p, tree1, tree2 = test_remove(10, tree1, tree2); points += p*2

        # Remove root with one child (5 points)
        tree1, tree2 = BST(), s.BST()
        tree1.insert(1); tree2.insert(1)
        tree1.insert(2); tree2.insert(2)
        tree1.insert(3); tree2.insert(3)
        tree1.insert(4); tree2.insert(4)
        tree1.insert(5); tree2.insert(5)
        tree1.insert(6); tree2.insert(6)
        p, tree1, tree2 = test_remove(1, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(2, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(3, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(4, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(5, tree1, tree2); points += p

        # Remove root with two children (5 points)
        tree1, tree2 = BST(), s.BST()
        tree1.insert(2); tree2.insert(2)
        tree1.insert(1); tree2.insert(1)
        tree1.insert(7); tree2.insert(7)
        tree1.insert(6); tree2.insert(6)
        tree1.insert(5); tree2.insert(5)
        tree1.insert(4); tree2.insert(4)
        tree1.insert(3); tree2.insert(3)
        p, tree1, tree2 = test_remove(2, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(3, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(4, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(5, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(6, tree1, tree2); points += p

        # Remove nonexistent (2 points)
        tree1, tree2 = load_trees()
        try:
            tree2.remove(0)
            self.feedback += "\n\tBST.remove(0) failed for 0 not in tree"
            self.feedback += "\nPrevious tree:\n" + str(tree1)
        except ValueError:
            points += 1

        try:
            tree2.remove(12.5)
            self.feedback += "\n\tBST.remove(12.5) failed for 12.5 not in tree"
            self.feedback += "\nPrevious tree:\n" + str(tree1)
        except ValueError:
            points += 1

        return points

    def problem4(self, s):
        """Test plot_times(). 10 points."""

        print("Running plot_times()...")
        s.plot_times("English.txt", 1000, 4000, 1000)
        points = -1
        while points > 10 or points < 0:
            try:
                points = int(input("\nScore out of 10: "))
            except:
                points  = -1
        if points != 10:
            self.feedback += "\n\t" + raw_input("Problem 4 feedback: ")

        return points
