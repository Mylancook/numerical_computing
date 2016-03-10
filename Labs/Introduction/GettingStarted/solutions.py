# solutions.py
"""Getting Started solutions file."""

# Problem 1: Modify this file so that it prints out "Hello, world!"
#  when it is run from the terminal or from a Python interpreter.


# Problem 2: Implement this function.
def sphere_volume(r):
    """Return the volume of the sphere of radius 'r'.
    Use 3.14159 for pi in your computation.
    """
    return (4 * 3.14159 / 3)*r**3


# Problem 3: Implement the first_half() and reverse() functions.
def first_half(my_string):
    """Return the first half of the string 'my_string'. Exclude the
    middle character if there are an odd number of characters.

    Examples:
        >>> first_half("python")
        'pyt'
        >>> first_half("ipython")
        'ipy'
    """
    return my_string[:len(my_string)//2]
    
def backward(my_string):
    """Return the reverse of the string 'my_string'.
    
    Examples:
        >>> backward("python")
        'nohtyp'
        >>> backward("ipython")
        'nohtypi'
    """
    return my_string[::-1]


# Problem 4: Implement this function.
def list_ops(my_list):
    """Perform the following operations on the list 'my_list':
        - Append "elephant".
        - Remove "ant"
        - Remove the entry at index 1.
        - Replace the entry at index 2 with "eagle".
        - Append "fox".

    Examples:
        >>> list_ops(["ant", "bear", "cat", "dog"])
        ['bear', 'dog', 'eagle', 'fox']
    """
    my_list.append("elephant")
    my_list.remove("ant")
    my_list.remove(my_list[1])
    my_list[2] = "eagle"
    my_list.append("fox")
    return my_list


# Problem 5: Implement this function.
def pig_latin(word):
    """Translate the string 'word' into Pig Latin
    
    Examples:
        >>> pig_latin("apple")
        'applehay'
        >>> pig_latin("banana")
        'ananabay'
    """
    if word[0] in "aeiou":
        return word + "hay"
    else:
        return word[1:] + word[0] + "ay"
        

# Problem 6: Implement this function.
def int_to_string(my_list):
    """Translate 'my_list', a list of numbers 1-26, to corresponding
    lowercase letters of the alphabet. 1 -> a, 2 -> b, 3 -> c, and so on.
    
    Example:
        >>> int_to_string([13, 1, 20, 8])
        ['m', 'a', 't', 'h'] 
    """
    my_dictionary = {1:'a',  2:'b',  3:'c',  4:'d',  5:'e',  6:'f',  7:'g',
                     8:'h',  9:'i', 10:'j', 11:'k', 12:'l', 13:'m', 14:'n',
                    15:'o', 16:'p', 17:'q', 18:'r', 19:'s', 20:'t', 21:'u',
                    22:'v', 23:'w', 24:'x', 25:'y', 26:'z'}
    output = []
    for number in my_list:
        output.append(my_dictionary[number])
    return output


# Problem 7: Implement this function.
def stringify(my_list):
    """Using a list comprehension, convert the list of integers 'my_list'
    to a list of strings. Return the new list.

    Example:
        >>> stringify([1, 2, 3])
        ['1', '2', '3']
    """
    return [str(n) for n in my_list]


# Problem 8: Implement this function and use it to approximate ln(2).
def alt_harmonic(n):
    """Return the partial sum of the first n terms of the alternating
    harmonic series. Use this function to approximae ln(2).
    """
    return sum([(-1)**(i+1)/float(i) for i in xrange(1,n)])


# Problem 1
if __name__ == '__main__':
    print("Hello, world!")

# ============================= END OF SOLUTIONS ============================ #

from os import system
from numpy.random import randint

# Test script        
def test(student_module):
    """Test script. Import the student's solutions file as a module.
    
     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
     5 points for problem 4
     5 points for problem 5
     5 points for problem 6
     5 points for problem 7
    10 points for problem 8
    
    Parameters:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 50.
        feedback (str): a printout of results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info.

    This and all other test drivers can be used to grade the entire lab
    assignment at once via test_all(), or to grade one problem at a time
    via the different problemX() functions.

    The point distribution is only a suggestion; the instructor may alter
    the weight of each problem as they see fit.
    """

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=50):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\nProblem %d (%d points):"%(number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += %d"%points
            except BaseException as e:
                self.feedback += "\n%s: %s"%(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem1, 1, 5)   # Problem 1:  5 points.
        test_one(self.problem2, 2, 5)   # Problem 2:  5 points.
        test_one(self.problem3, 3, 10)  # Problem 3: 10 points.
        test_one(self.problem4, 4, 5)   # Problem 4:  5 points.
        test_one(self.problem5, 5, 5)   # Problem 5:  5 points.
        test_one(self.problem6, 6, 5)   # Problem 6:  5 points.
        test_one(self.problem7, 7, 5)   # Problem 7:  5 points.
        test_one(self.problem8, 8, 10)  # Problem 8: 10 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(
                                    self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n%s'%comments

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if correct == student:
            return 1
        else:
            self.feedback += message
            self.feedback += "\n\tCorrect response: %s"%correct
            self.feedback += "\n\tStudent response: %s"%student
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of %d: "%points))
            except:
                credit = -1
        if credit != points:
            # Comment on what was lacking (optionally).
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n%s"%comments
            elif message is not None:
                self.feedback += message
        return credit

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test Hello, world! printout. 5 points."""

        print("Testing 'Hello, world!' printout:")
        system("python " + s.__file__)
        return self._grade(5, "\n'Hello, world!' failed to print.")

    def problem2(self, s):
        """Test sphere_volume(). 5 Points."""
        if not hasattr(s, "sphere_volume"):
            raise NotImplementedError("Problem 2 Incomplete")
        if s.sphere_volume(1) is None:
            raise NotImplementedError("sphere_volume() returned nothing")
        
        points  = 2*self._eqTest(sphere_volume(5), s.sphere_volume(5),
                                            "\nsphere_volume(5) failed")
        points += 3*self._eqTest(sphere_volume(3.14), s.sphere_volume(3.14),
                                            "\nsphere_volume(3.14) failed")
        return points

    def problem3(self, s):
        """Test first_half() and backward(). 10 points."""
        if not hasattr(s, "first_half") or not hasattr(s, "backward"):
            raise NotImplementedError("Problem 3 Incomplete")
        if s.first_half("abcde") is None:
            raise NotImplementedError("first_half() returned nothing")
        if s.backward("abcde") is None:
            raise NotImplementedError("backward() returned nothing")

        points  = 2*self._eqTest(first_half("abcde"), s.first_half("abcde"),
                                            "\nfirst_half('abcde') failed")
        points += 3*self._eqTest(first_half("TK421"), s.first_half("TK421"),
                                            "\nfirst_half('TK421') failed")
        points += 2*self._eqTest(backward("abcde"), s.backward("abcde"),
                                            "\nfirst_half('abcde') failed")
        points += 3*self._eqTest(backward("TK421"), s.backward("TK421"),
                                            "\nfirst_half('TK421') failed")
        return points

    def problem4(self, s):
        """Test list_ops(). 5 points."""
        if not hasattr(s, "list_ops"):
            raise NotImplementedError("Problem 4 Incomplete")
        if s.list_ops(["ant", "bear", "cat", "dog"]) is None:
            raise NotImplementedError("list_ops() returned nothing")
        
        points = 2*self._eqTest(  list_ops(["ant", "bear", "cat", "dog"]),
                                s.list_ops(["ant", "bear", "cat", "dog"]),
                        '\nlist_ops(["ant", "bear", "cat", "dog"]) failed')
        points +=3*self._eqTest(list_ops(["ant", "beaver", "cobra", "dragon"]),
                            s.list_ops(["ant", "beaver", "cobra", "dragon"]),
                '\nlist_ops(["ant", "beaver", "cobra", "dragon"]) failed')
        return points

    def problem5(self, s):
        """Test pig_latin(). 5 points."""
        if not hasattr(s, "pig_latin"):
            raise NotImplementedError("Problem 5 Incomplete")
        if s.pig_latin("piglatin") is None:
            raise NotImplementedError("pig_latin() returned nothing")

        points = 2*self._eqTest(  pig_latin("college"),
                                s.pig_latin("college"),
                                            "\npig_latin('college') failed")
        points += 3*self._eqTest(  pig_latin("university"),
                                 s.pig_latin("university"),
                                        "\npig_latin('university') failed")
        return points

    def problem6(self, s):
        """Test int_to_string(). 5 points.""" 
        if not hasattr(s, "int_to_string"):
            raise NotImplementedError("Problem 6 Incomplete")
        if s.int_to_string([1]) is None:
            raise NotImplementedError("int_to_string() returned nothing")
        
        points = 2*self._eqTest(int_to_string([1, 2, 3]),
                                s.int_to_string([1, 2, 3]),
                                    "\nint_to_string([1, 2, 3]) failed")
        points += 3*self._eqTest(
                        int_to_string([24, 25, 12, 15, 16, 8, 15, 14, 5]),
                        s.int_to_string([24, 25, 12, 15, 16, 8, 15, 14, 5]),
            "\nint_to_string([24, 25, 12, 15, 16, 8, 15, 14, 5]) failed")
        return points

    def problem7(self, s):
        """Test stringify(). 5 points."""
        if not hasattr(s, "stringify"):
            raise NotImplementedError("Problem 7 Incomplete")
        if s.stringify([1]) is None:
            raise NotImplementedError("stringify() returned nothing")
        
        points = 2*self._eqTest(stringify([1, 2, 3]), s.stringify([1, 2, 3]),
                                            "\nstringify([1, 2, 3]) failed")

        rand_list = ['start'] + list(randint(1,10,10)) + ['end']
        points += 3*self._eqTest(stringify(rand_list), s.stringify(rand_list),
                            "\nstringify(" + str(rand_list) + ") failed")
        return points

    def problem8(self, s):
        """Test alt_harmonic(). 10 points."""
        if not hasattr(s, "alt_harmonic"):
            raise NotImplementedError("Problem 8 Incomplete")
        if s.alt_harmonic(10) is None:
            raise NotImplementedError("alt_harmonic() returned nothing")

        points = 4*self._eqTest(alt_harmonic(100), s.alt_harmonic(100),
                                            "\nalt_harmonic(100) failed")
        points += 6*self._eqTest(alt_harmonic(5000), s.alt_harmonic(5000),
                                            "\nalt_harmonic(5000) failed")
        return points
