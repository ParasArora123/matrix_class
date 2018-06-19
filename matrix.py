import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I
    
def get_row(matrix, row):
    """
    get a specific row from a matrix  
    """
    return matrix[row]
    
def get_column(matrix, column_number):
    """
    get a specific column from a matrix
    """
    column = []

    for i in range(len(matrix)):
        # column number must stay static while row is changing
        # so it will look like: matrix[0][0], matrix[1][0], matrix[2][0] etc.  
        column.append(matrix[i][column_number])

    return column            
    
def dot_product(vector_one, vector_two):
    """
    caculate the dot product of two vectors 
    """
    # in order to 'dot_product' vectors they must be the same size
    if len(vector_one) == len(vector_two):

        sum_vectors = 0
        for i in range(len(vector_one)):
            sum_vectors += vector_one[i] * vector_two[i] # multiplying each element at the same place within each vector

    return sum_vectors        

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            return self.g[0][0] # The determinant of a 1x1 is simply the value within the matrix 
        elif self.h == 2:
            # Putting each number in variables to make it easier to read
            a, b, c, d = self.g[0][0], self.g[0][1], self.g[1][0], self.g[1][1]
            return a*d - b*c 

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        
        trace_mat = 0

        # Nested for loop, looping through the matrix 
        for i in range(self.h):
            for j in range(self.w):

                # It is on the diagnol when the row = col
                if i == j:
                    trace_mat += self[i][j]

        return trace_mat

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        inverse = [] # the final inverted matrix
        
        if self.h == 1:
            inverse.append([1/self.g[0][0]]) # simply need to do 1/element to invert a 1x1 matrix
            
        elif self.h == 2:
            # putting each number into a variable to make it easier to read
            a, b, c, d = self.g[0][0], self.g[0][1], self.g[1][0], self.g[1][1]
            
            if a*d != b*c:
                
                # setting inverse to the current matrix and then going step by step
                # changing each part necessary to achieve the correct inverted matrix
                inverse = self.g 
                
                determinant = (a*d) - (b*c)
                first_term = 1/determinant 
                
                # filling inverse to achieve the [[d, -b], [-c, a]] part of the equation
                inverse[0][0] = d
                inverse[0][1] = -1*b
                inverse[1][0] = -1*c
                inverse[1][1] = a
                
                # Change every number in inverse by the first term in the equation (1/determinant)
                for i in range(len(inverse)):
                    for j in range(len(inverse)):
                        inverse[i][j] *= first_term
            else:
                raise(RuntimeError, "a*d is equal to b*c so there is no inverse of this matrix!!") 
                
        return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = []
        
        
        # Nested for loop, but since we want to transpose it
        # we want to flip the rows and columns. To do this
        # I went through the number of columns first (matrix[0])
        # and then the number of rows, building a new matrix with
        # the flipped number of rows and columns 
        
        for i in range(self.w):
            new_row = [] 
            
            for j in range(self.h):
                new_row.append(self[j][i]) # may have to change to grid[j][i]
            matrix_transpose.append(new_row) # must complete one row at a time
        
        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
            
        matrixSum = [] # matrix to hold the results
        
        for i in range(self.h):
            new_row = [] # emptying new_row each time a row is appended
            
            for j in range(self.w):
                num = self.g[i][j] + other.g[i][j] # adding the numbers at the corresponding places in the matricies
                new_row.append(num)
            matrixSum.append(new_row)
        
        return Matrix(matrixSum)


    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        neg_mat = []
        for i in range(self.h):
            new_row = [] # Emptying new_row each time after appended to neg_mat
            
            for j in range(self.w):
                new_row.append(self.g[i][j] * -1) # multiplying each value in self by -1 then appending
            neg_mat.append(new_row)
                
        return Matrix(neg_mat)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        matrixFinal = [] # matrix to hold the results
        
        for i in range(self.h):
            new_row = [] # emptying new_row each time a row is appended
            
            for j in range(self.w):
                num = self.g[i][j] - other.g[i][j] # subtracting the numbers at the corresponding places in the matricies
                new_row.append(num)
            matrixFinal.append(new_row)
        
        return Matrix(matrixFinal)
    
    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        
        m_rows = self.h
        p_columns = other.w

        # empty list that will hold the product of AxB
        result = []

        for i in range(m_rows):
            row_result = [] # Adding rows one at a time
            for j in range(p_columns):
                # creating vectors that will be multiplied using a row of 'self' and col of 'other'
                row = get_row(self.g, i)
                col = get_column(other.g, j)

                row_result.append(dot_product(row, col)) # finding the dot product of vectors row and col and appending
            result.append(row_result)

        return Matrix(result)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
        
            final_mat = []
            for i in range(self.h):
                new_row = [] # empyting new_row each time after appended
                
                for j in range(self.w):
                    new_row.append(self.g[i][j] * other) # multiplying each value in self by other than appending to the row
                final_mat.append(new_row)
                
            return Matrix(final_mat) 
                    
                
            