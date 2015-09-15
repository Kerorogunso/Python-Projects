from __future__ import division
from matplotlib import pyplot as plt 
import random

num_friends = [random.randrange(1,100) for _ in range(200)]
xs = range(101)
ys = [num_friends[x] for x in xs]
plt.bar(xs,ys)
plt.axis([0,101,0,100])
plt.title("Histogram of friend counts")
plt.xlabel("# of friends")
plt.ylabel("# of people")
plt.show()

num_points = len(num_friends)
largest_value = max(num_friends)
smallest_value = min(num_friends)

sorted_values = sorted(num_friends)
smallest_value = sorted_values[0]
second_smallest_value = sorted_values[1]
second_largest_value = sorted_values[-2]

def mean(x):
	return sum(x)/len(x)

print mean(num_friends)

def median(x):
	n = len(x)
	xsort = sorted(x)
	mid = n//2

	if n%2 != 0:
		return xsort[mid]
	else:
		return mean([xsort[mid - 1],xsort[mid]])

def quantile(x,p):
	# returns the pth-percentile value in x
	p_index = int(p * len(x))
	return sorted(x)[p_index]

def mode(x):
	counts = Counter(x)
	max_count = max(counts.values())
	return [x_i for x_i, count in counts.iteritems() if count == max_count]

def data_range(x):
	return max(x) - min(x)

def de_mean(x):
	x_bar = mean(x)
	return [x_i - x_bar for x_i in x]

def variance(x):
	n = len(x)
	deviations = de_mean(x)
	return sum(d**2 for d in deviations) / (n-1)

def standard_deviation(x):
	return math.sqrt(variance(x))

def interquartile_range(x):
	return quantile(x,0.75) - quantile(x,0.25)

def covariance(x,y):
	n = len(x)
	dx = de_mean(x)
	dy = de_mean(y)
	return sum(x_i * y_i for x_i,y_i in zip(dx,dy))/(n-1)

def correlation(x,y):
	stdev_x = standard_deviation(x)
	stdev_y = standard_deviation(y)

	if stdev_x > 0 and stdev_y > 0:
		return covariance(x,y)/(stdev_y * stdev_x)
	else:
		return 0

		