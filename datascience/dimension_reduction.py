from __future__ import division
from linear_algerbra import shape, mean, get_column, magnitude, dot, scalar_multiply
from statistics import standard_deviation
from gradient_descent import maximize_batch
from functools import partial

def scale(data_matrix):
	"""returns the means and standard deviations of each column"""
	num_rows, num_cols = shape(data_matrix)
	means = [mean(get_column(data_matrix, j)) for j in range(num_cols)]
	stdevs = [standard_deviation(get_column(data_matrix, j)) for j in range(num_cols)]

	return means, stdevs

def rescale(data_matrix):
	"""rescales the input data so that each column has mean 0
	and standard deviation 1, leaves columns alone with no
	deviations"""
	means, stdevs = scale(data_matrix)

	def rescaled(i, j):
		if stdevs[j] > 0:
			return (data_matrix[i][j] - means[j]) / stdevs[j]
		else:
			return data_matrix[i][j]

	num_rows, num_cols = shape(data_matrix)
	return make_matrix(num_rows, num_cols, rescaled)

def de_mean_matrix(A):
	"""returns the result of subtracting from every value in A
	the mean value of its column. the resulting matrix has mean 0
	in every column"""
	nr, nc = shape(A)
	column_means, _ = scale(A)
	return make_matrix(nr, nc, lambda i, j: A[i][j] - column_means[j])

def direction(w):
	mag = magnitude(w)
	return [w_i / mag for w_i in w]

def directional_variance_i(x_i, w):
	"""the variance of the row x_i in the direction determined by w"""
	return dot(x_i, direction(w)) ** 2

def directional_variance(X,w):
	"""the variance of the data in the direction determined by w"""
	return sum(directional_variance_i(x_i, w) for x_i in X)

def directional_variance_gradient_i(x_i, w):
	"""the contribution of row x_i to the gradient of the direction-w variance"""
	projection_length = dot(x_i, direction(w))
	return [ 2 * projection_length * x_ij for x_ij in x_i]

def directional_variance_gradient(X, w):
	return vector_sum(directional_variance_gradient_i(x_i, w) for x_i in X)

def first_principal_component(X):
	guess = [1 for _ in X[0]]
	unscaled_maximizer = maximize_batch(
		partial(directional_variance, X),
		partial(directional_variance_gradient, X),
		guess)
	return direction(unscaled_maximizer)

# here there is no "y" so we just pass in a vector of Nones
# and functions that ignore that input

def first_principal_component_sgd(X):
	guess = [1 for _ in X[0]]
	unscaled_maximizer = maximize_stochastic(
		lambda x, _, w: directional_variance_i(x, w),
		lambda x, _, w: directional_variance_gradient_i(x, w),
		X,
		[None for _ in X], # the fake "y"
		)
	return direction(unscaled_maximizer)

def project(v, w):
	"""return the projection of v onto the direction w"""
	projection_length = dot(v, w)
	return scalar_multiply(projection_length, w)

def remove_projection_from_vector(v, w):
	"""projects v onto w and subtracts the result from v"""
	return vector_subtract(v, project(v, w))

def remove_projection(X, w):
	"""for each row of X, project the row onto w, and subtract the result from the row"""
	return [remove_projection_from_vector(x_i, w) for x_i in X]

def principal_component_analysis(X, num_components):
	components = []
	for _ in range(num_components):
		component = first_principal_component(X)
		components.append(component)
		X = remove_projection(X component)

	return components

def transform_vector(v, components):
	return [dot(v, w) for w in components]

def transform(X, components):
	return [transform_vector(x_i, components) for x_i in X]
	