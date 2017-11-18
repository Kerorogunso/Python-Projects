from __future__ import division
from Probability import normal_cdf, inverse_normal_cdf
import math
import random


def normal_approximation_to_binomial(n, p):
	""" finds m and sigma corresponding to Binomial(n,p) """

	mu = p * n
	sigma = math.sqrt(n * p * (1-p))
	return mu,sigma

# the normal cdf is the probability the variable is below a threshold
normal_probability_below = normal_cdf

# it's above the threshold if it's not below the threshold
def normal_probability_above(lo, mu=0, sigma=1):
	return 1 - normal_cdf(lo, mu, sigma)

# it's between if its less than hi, but not less than lo
def normal_probability_between(lo, hi, mu=0, sigma=1):
	return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)

# it's outside if it's not between
def normal_probability_outside(lo, hi, mu=0, sigma=1):
	return 1 - normal_probability_between(lo, hi, mu, sigma)

def normal_upper_bound(probability, mu=0, sigma=1):
	"""returns the z for which P(Z <= z) = probability"""
	return inverse_normal_cdf(probability, mu, sigma)

def normal_lower_bound(probability, mu=0, sigma=1):
	"""return the z for which P(Z >= z) = probability"""
	return inverse_normal_cdf(1 - probability, mu, sigma)

def normal_two_sided_bounds(probability, mu=0, sigma=1):
	"""returns the symmetric (about the mean) bounds that contain the specified probability"""
	tail_probability = (1 - probability) / 2

	# upper bound should have tail_probability above it
	upper_bound = normal_lower_bound(tail_probability, mu, sigma)

	# lower bound should have tail_probability above it
	lower_bound = normal_upper_bound(tail_probability, mu, sigma)

	return lower_bound, upper_bound

mu_0, sigma_0 = normal_approximation_to_binomial(1000,0.5)


normal_two_sided_bounds(0.95,mu_0,sigma_0)

# 95% of bounds based on assumption p = 0.5
lo, hi = normal_two_sided_bounds(0.95,mu_0,sigma_0)

# actual mu and sigma based on p = 0.55
mu_1, sigma_1 = normal_approximation_to_binomial(1000,0.55)

# a type 2 error means we fail to reject the null hypothesis which will
# happen when X is still in our original interval

type_2_probability = normal_probability_between(lo,hi,mu_1,sigma_1)
power = 1 - type_2_probability

def two_sided_p_value(x, mu=0, sigma=1):
	if x >= mu:
		# if x is greater than the mean, the tail is what's greater than x
		return 2 * normal_probability_above(x,mu,sigma)
	else:
		# if x is less than the mean, the tail is what's less than x
		return 2 * normal_probability_below(x,mu,sigma)

print two_sided_p_value(529.5,mu_0,sigma_0)

extreme_value_count = 0

for _ in range(100000):
	num_heads = sum(1 if random.random() < 0.5 else 0 for _ in range(1000))			# in 1000 flips
	if num_heads >= 530 or num_heads <= 470:
		extreme_value_count += 1

print extreme_value_count / 100000				

# Confidence intervals after observing 525 heads.
p_hat = 525 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000) # 0.0158

normal_two_sided_bounds(0.95,mu,sigma) # [0.4940,0.5560]

# 95% of the time true value of p lies in this interval. 0.5 in this
# interval so does not reject that coin is unfair.

# If we see 545 heads.
p_hat = 545 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000) # 0.0158

normal_two_sided_bounds(0.95,mu,sigma) # [0.5091, 0.5709]

# Fair coin does not lie in this confidence interval.

def run_experiment():
	""" flip a fair coin 1000 times, True = heads, False = tails"""
	return [random.random() < 0.5 for _ in range(1000)]

def reject_fairness(experiment):
	""" using 5% significant levels """
	num_heads = len([flip for flip in experiment if flip])

	return num_heads < 469 or num_heads > 531

random.seed(0)
experiments = [run_experiment() for _ in range(1000)]
num_rejections = len([experiment for experiment in experiments
 					  if reject_fairness(experiment)])

print num_rejections

def estimated_parameters(N,n):
	p = n / N
	sigma = math.sqrt(p * (1 - p) / N)
	return p, sigma

def a_b_test_statistic(N_A,n_A,N_B,n_B):
	p_A, sigma_A = estimated_parameters(N_A,n_A)
	p_B, sigma_B = estimated_parameters(N_B,n_B)
	return (p_A - p_B) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)	

# 200 people click on ad A, 180 people click on ad B
z = a_b_test_statistic(1000,200,1000,180) # -1.14

# probability of seeing this difference if the means were equal.
prob = two_sided_p_value(z) # 0.254

# This is greater than 0.05 so can't conclude there is much of a difference.

z = a_b_test_statistic(1000,200,1000,150) # -2.94
prob = two_sided_p_value(z) # 0.003

# Only a probability of observing this z if the ads were equally effective.

# Form prior from the Beta distribution.

def B(alpha,beta):
	"""a normalizing constant so that the total probability is 1"""
	return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)

def beta_pdf(x, alpha, beta):
	if x < 0 or x > 1:
		return 0

	return x ** (alpha - 1) + (1 - x) ** (beta - 1) / B(alpha,beta)