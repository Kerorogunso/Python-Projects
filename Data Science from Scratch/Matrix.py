A = [[1,2,3],
	 [4,5,6]]

B = [[1,2],
	 [3,4],
	 [5,6]]

def shape(A):
	num_rows = len(A)
	num_cols= len(A[0]) if A else 0

	return [num_rows,num_cols]

def get_row(A,i):
	return A[i] if shape(A)[0] >= i else None

def get_column(A,j):
	return [A_i[j] for A_i in A if shape(A)[1] >= j]

def make_matrix(num_rows,num_cols,entry_fn):
	""" returns a num_rows x num_cols matrix whose (i,j)th entry is entry_fn(i,j)"""
	return [[entry_fn(i,j) for j in range(num_cols)] for i in range(num_rows)]

def is_diagonal(i, j):
	return 1 if i == j else 0

identity_matrix = make_matrix(5,5,is_diagonal)
