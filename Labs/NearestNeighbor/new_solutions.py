# new_solutions.py
"""Volume II Lab 7: Nearest Neighbor Search. Solutions file.

< IN DEVELOPMENT >

"""

# =================== BSTNode / BST Classes from Trees.py =================== #
class BSTNode(object):
    def __init__(self, data):
        self.value = data
        self.prev = None
        self.left = None
        self.right = None

class BST(object):
    def __init__(self):
        self.root = None
    
    def __str__(self):
        if self.root is None:
            return "[]"
        str_tree = [list() for i in xrange(_height(self.root) + 1)]
        visited = set()
        
        def _visit(current, depth):
            str_tree[depth].append(current.value)
            visited.add(current)
            if current.left and current.left not in visited:
                _visit(current.left, depth+1)
            if current.right and current.right not in visited:
                _visit(current.right, depth+1)
        
        _visit(self.root, 0)
        out = ""
        for level in str_tree:
            if level != list():
                out += str(level) + "\n"
            else:
                break
        return out

def _height(current):
    if current is None:
        return -1
    return 1 + max(_height(current.right), _height(current.left))

# ============================== solutions.py =============================== #

import numpy as np
from sklearn import neighbors
from scipy.spatial import KDTree


# Problem 1: Implement this function.
def metric(x, y):
    """Return the euclidean distance between the 1-D arrays 'x' and 'y'.

    Raises:
        ValueError: if 'x' and 'y' have different lengths.
    
    Example:
        >>> metric([1,2],[2,2])
        1.0
        >>> metric([1,2,1],[2,2])
        ValueError: Incompatible dimensions.
    """
    if len(x) != len(y):
        raise ValueError("Incompatible dimensions.")
    return np.linalg.norm(x - y)
    
    # Or a slightly longer way:
    return np.sqrt(np.sum((x - y)**2))
    # Or the longest/worst way:
    total = 0
    for i in xrange(len(x)):
        term = x[i] - y[i]
        total += term**2
    total = np.sqrt(total)
    return total


# Problem 2: Implement this function.
def exhaustive_search(data_set, target):
    """Solve the nearest neighbor search problem exhaustively.
    Check the distances between 'target' and each point in 'data_set'.
    Use the Euclidean metric to calculate distances.
    
    Inputs:
        data_set (mxk ndarray): An array of m k-dimensional points.
        target (1xk ndarray): A k-dimensional point to compare to 'dataset'.
        
    Returns:
        the member of 'data_set' that is nearest to 'target' (1xk ndarray).
        The distance from the nearest neighbor to 'target' (float).
    """

    # Initialize the outputs.
    minimum_distance = float("inf")
    nearest_neighbor = None

    # Search through the entire data set for the nearest neighbor.
    for point in data_set:
        distance = metric(target, point)
        if distance < minimum_distance:
            nearest_neighbor = point
            minimum_distance = distance

    return nearest_neighbor, minimum_distance


# Problem 3: Add magic methods to this class.
class KDTNode(BSTNode):
    """Node class for K-D Trees. Inherits from BSTNode.

    Attributes:
        left (KDTNode): a reference to this node's left child.
        right (KDTNode): a reference to this node's right child.
        parent (KDTNode): a reference to this node's parent node.
        data (ndarray): a coordinate in k-dimensional space.
        axis (int): the 'dimension' of the node to make comparisons on.
    """

    def __init__(self, data):
        """Construct a K-D Tree node containing 'data'. The left, right,
        and prev attributes are set in the constructor of BSTNode.

        Raises:
            TypeError: if 'data' is not a NumPy array (of type np.ndarray).
        """
        if type(data) != np.ndarray:
            raise TypeError("A NumPy array or a list is required.")
        BSTNode.__init__(self, data)
        self.axis  = 0

    # Defining these magic methods is not required, but may be useful.    
    def __sub__(self, other):
        return metric(self.value, other.value)

    def __eq__(self, other):
        return np.allclose(self.value, other.value)

    def __repr__(self):
        return str(self.value)

# Problem 4: Finish implementing this class by overriding
#            the __init__(), insert(), and remove() methods.
class KDT(BST):
    """A k-dimensional binary search tree object.
    Used to solve the nearest neighbor problem efficiently.

    Attributes:
        root (KDTNode): the root node of the tree. Like all other
            nodes in the tree, the root houses data as a NumPy array.
        k (int): the dimension of the tree (the 'k' of the k-d tree).
    """

    def __init__(self, data_set):
        """Set the k attribute and fill the tree with the points
        in 'data_set'. Raise a TypeError if the input is not a NumPy
        array.
        """
        BST.__init__(self)
        if not isinstance(data_set, np.ndarray):
            raise TypeError("data_set must be a NumPy array.")
        self.k = data_set.shape[1]
        for point in data_set:
            self.insert(point)
    
    def find(self, data):
        """Return the node containing 'data'.

        Raises:
            ValueError: if there is no node containing 'data' in the tree.
        """
        
        def _step(current):
            """Recursively approach the target array in the tree."""
            
            if current is None:         # Base case: target is not in the tree.
                raise ValueError(str(data) + " is not in the tree")
            elif np.allclose(data, current.value):
                return current                      # Base case: target found!
            elif data[current.axis] < current.value[current.axis]:
                return _step(current.left)          # Recursively search left.
            else:
                return _step(current.right)         # Recursively search right.
            
        return _step(self.root)
    
    def insert(self, data):
        """Insert a new node containing 'data' at the appropriate location.
        Return the new node. This method should be similar to BST.insert().
        """

        # Check that the data matches the dimension of the tree.
        if len(data) != self.k:
            raise ValueError("data must have {} entries".format(self.k))
        
        # Create the node to be inserted.
        new_node = KDTNode(data)
        
        def _find_parent(current):
            """Recursively descend through the tree to find the node that
            should be the parent of the new node. Do not allow for duplicates.
            """

            # Base case: error (shouldn't happen).
            assert current is not None, "_find_parent() error"
            # Base case: duplicate values.
            if np.allclose(data, current.value):  
                raise ValueError("{} is already in the tree".format(data))
            # Look to the left.
            elif data[current.axis] < current.value[current.axis]:
                # Recurse on the left branch.
                if current.left is not None:
                    return _find_parent(current.left)
                # Base case: insert the node on the left.
                else:
                    current.left = new_node
            # Look to the right.
            else:
                # Recurse on the right branch.
                if current.right is not None:
                    return _find_parent(current.right)
                # Base case: insert the node on the right.
                else:       
                    current.right = new_node
            return current
        
        # Case 1: The tree is empty. Assign the root and axis appropriately.
        if self.root is None:
            self.root = new_node
            new_node.axis = 0

        # Case 2: The tree is nonempy. Use _find_parent() and double link.
        else:
            # Find the parent and insert the new node as its child.
            parent = _find_parent(self.root)

            # Double-link the child to its parent and set its axis attribute.
            new_node.prev = parent
            new_node.axis = (parent.axis + 1) % self.k
    
    def remove(*args, **kwargs):
        raise NotImplementedError("'remove()' has been disabled.")


# Problem 5: Implement this function
def nearest_neighbor(data_set, target):
    """Use your KDTree class to solve the nearest neighbor problem.

    Inputs:
        data_set ((m,k) ndarray): An array of m k-dimensional points.
        target ((k,) ndarray): A k-dimensional point to compare to 'dataset'.

    Returns:
        The point in the tree that is nearest to 'target' ((k,) ndarray).
        The distance from the nearest neighbor to 'target' (float).
    """
    
    def KDsearch(current, neighbor, distance):
        """The actual nearest neighbor search algorithm.
        
        Inputs:
            current (KDTNode): the node to examine.
            neighbor (KDTNode): the current nearest neighbor.
            distance (float): the current minimum distance.

        Returns:
            neighbor (KDTNode): The new nearest neighbor in the tree.
            distance (float): the new minimum distance.
        """
        
        # Base case. Return the distance and the nearest neighbor.
        if current is None:
            return neighbor, distance
        index = current.axis
        d = metric(target, current.value)
        if d < distance:
            distance = d
            neighbor = current
        if target[index] < current.value[index]: # Recursively search 'left'
            neighbor, distance = KDsearch(
                current.left, neighbor, distance)
                                    # Back up if needed
            if target[index] + distance >= current.value[index]:
                neighbor, distance = KDsearch(
                    current.right, neighbor, distance)
        else:                       # Recursively search 'right'
            neighbor, distance = KDsearch(
                current.right, neighbor, distance)
                                    # Back up if needed
            if target[index] - distance <= current.value[index]: # (?)
                neighbor, distance = KDsearch(
                    current.left, neighbor, distance)
    
        return neighbor, distance
    
    # Load and search the KD-Tree.
    tree = KDT(data_set)
    start_distance = metric(tree.root.value, target)
    node, dist = KDsearch(tree.root, tree.root, start_distance)
    return node.value, dist

def postal_problem(grading=False):
    """Use the neighbors module in sklearn to classify the Postal data set
    provided in 'PostalData.npz'. Classify the testpoints with 'n_neighbors'
    as 1, 4, or 10, and with 'weights' as 'uniform' or 'distance'. For each
    trial print a report indicating how the classifier performs in terms of
    percentage of correct classifications. Which combination gives the most
    correct classifications?

    Your function should print a report similar to the following:
    n_neighbors = 1, weights = 'distance':  0.903
    n_neighbors = 1, weights =  'uniform':  0.903       (...and so on.)
    """
    if grading:
        print "n_neighbors =  1, weights = 'distance':\t0.903"
        print "n_neighbors =  1, weights = 'uniform' :\t0.903"
        print "n_neighbors =  4, weights = 'distance':\t0.906"
        print "n_neighbors =  4, weights = 'uniform' :\t0.89"
        print "n_neighbors = 10, weights = 'distance':\t0.912 (best)"
        print "n_neighbors = 10, weights = 'uniform' :\t0.903"
        return

    labels, points, testlabels, testpoints = np.load('PostalData.npz').items()

    def trial(n, w):
        nbrs = neighbors.KNeighborsClassifier(n_neighbors=n, weights=w, p=2)
        nbrs.fit(points[1], labels[1])
        prediction = nbrs.predict(testpoints[1])
        return np.average(prediction/testlabels[1])

    print "n_neighbors =  1, weights = 'distance':\t", trial(1, 'distance')
    print "n_neighbors =  1, weights = 'uniform' :\t", trial(1, 'uniform')
    print "n_neighbors =  4, weights = 'distance':\t", trial(4, 'distance')
    print "n_neighbors =  4, weights = 'uniform' :\t", trial(4, 'uniform')
    print "n_neighbors = 10, weights = 'distance':\t", trial(10, 'distance')
    print "n_neighbors = 10, weights = 'uniform' :\t", trial(10, 'uniform')

# ============================= END OF SOLUTIONS ============================ #

'''
from matplotlib import pyplot as plt

def makeplots():
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(0,10), ylim=(0,10))

    point_list = [(5,5), (8,4), (3,2), (7,7), (2,6), (9,2), (4,7)]
    x = [5, 8, 3, 7, 2, 9, 4]
    y = [5, 4, 2, 7, 6, 2, 7]
    ax.axvline(5, 0, 1)
    ax.axhline(4, .5, 1, color='r')
    ax.axhline(2, 0, .5, color='r')
    ax.axvline(7, .4, 1)
    ax.axvline(2, .2, 1)
    ax.axvline(9, 0, .4)
    ax.axhline(7, .2, .5, color="r")
    #plt.annotate("root", xy=(5,5), xytext=(5.2,5))
    #plt.annotate("root.right", xy=(8,4), xytext=(7.65,4.35))
    #plt.annotate("root.right.left", xy=(9,2), xytext=(7,2))
    #plt.annotate("root.left", xy=(3,2), xytext=(2.65,1.6))
    #plt.annotate("root.left.right", xy=(1,6), xytext=(.2,6.1))
    #plt.annotate("root.left.right.right\n     (new node)", xy=(4,7),
    #                                        xytext=(2.35,7.3))

    ax.plot(x, y, 'ok')
    ax.plot([8], [4.45], '*k')
    mid = plt.Circle(xy=(8,4), radius=.5, color="green", alpha=.3)
    upp = plt.Circle(xy=(7,7), radius=.5, color="purple", alpha=.3)
    ax.add_artist(mid)
    ax.add_artist(upp)
    plt.annotate("target", xy=(8,4.5), xytext=(8.2,4.5))
    plt.show()

if __name__ == '__main__':
    makeplots()
'''

# =============================== END OF FILE =============================== #
