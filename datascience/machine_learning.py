from __future__ import division
import random

def split_data(data, prob):
	"""split data into fractions [prob, 1 - prob]"""
	results = [],[]
	for row in data:
		results[0 if random.random() < prob else 1].append(row)
    return results

def train_test_split(x, y, test_pct):
	data = zip(x, y)                                # pair corresponding values
	train, test = split_data(data, 1 - test_pct)    # split the data set of pairs
	x_train, y_train = zip(*train)                  # magical un-zip trick
    x_test, y_test = zip(*test)

    return x_train, y_train, x_test, y_test

def accuracy(tp, fp, fn, tn):
	correct = tp + tn
	total = tp + fp + fn + tn
	return correct / total

def precision(tp, fp, fn, tn):
	return tp / (tp + fp)

def recall(tp, fp, fn, tn):
	return tp / (tp + fn)

def f1_score(tp, fp, fn, tn):
	p = precision(tp, fp, fn, tn)
	r = recall(tp, fp, fn, tn)

	return 2 * p * r / (p + r)