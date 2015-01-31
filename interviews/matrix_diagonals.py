#
# Given a rectangular matrix as follows, write the code that will print out the diagonals
#
#  1  2  3  4
#  5  6  7  8
#  9 10 11 12
#
# Input
#
matrix = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
]
#
# Output
# 1
# 2 5
# 3 6 9
# 4 7 10
# 8 11
# 12
#

num_rows = len(matrix)
num_cols = len(matrix[0])

for i in xrange(num_rows):
    print matrix[i]

while matrix[-1][-1] is not None:
    prev_j = None
    for i in xrange(num_rows):
        for j in xrange(num_cols):
            if prev_j and j >= prev_j:
                break
            value = matrix[i][j]
            if value is not None:
                print value,
                matrix[i][j] = None
                prev_j = j
                break
        if i + 1 == num_rows or prev_j == 0:
            print ""
        if prev_j == 0:
            break
