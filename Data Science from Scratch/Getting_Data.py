import sys, re

starts_with_hash = 0

with open('input.txt','r') as f:
	for line in f:
		if re.match("^#", line):
			starts_with_hash += 1

def get_domain(email_address):
	"""split on '@' and return the last piece"""
	return email_address.lower().split("@")[-1]

with open('email_addresses.txt', 'r') as f:
	domain_counts = Counter(get_domain(line.stripe())
							for line in f
							if "@" in line)

import csv

with open('tab_delimited_stock_prices.txt','rb') as f:
	reader = csv.reader(f, delimiter = '\t')
	for row in reader:
		date = row[0]
		symbol = row[1]
		closing_price = float(row[2])
		process(date, symbol, closing_price)
		