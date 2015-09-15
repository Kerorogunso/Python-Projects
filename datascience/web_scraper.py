import sys, re
from bs4 import BeautifulSoup
from time import sleep
import requests
from collections import Counter

# Takes a html webpage and a keyword and re
def word_finder(text,keyword):
	
	# Regular expression for finding the exact word.
	regex = "\\b" + keyword + "\\b"

	with open(text,'r') as f:
		for line in f:
			if re.search(regex,line.lower()):
				print line

#text_file = raw_input("Please enter the filename you wish to look in: ")
#word = raw_input("Please enter the keyword you want to find: ")

#print "We found these lines had the keyword you were looking for: "
#word_finder(text_file, word)

url = "http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationonDate&page=1"
soup = BeautifulSoup(requests.get(url).text,'html5lib')

# Gets all the td elements with thumbtext class
tds = soup('td', 'thumbtext')
print len(tds)

def is_video(td):
	"""it's a video if it has exactly one pricelabel, and if the
	stripped text inside that pricelabel starts with 'Video'"""
	pricelabels = td('span', 'pricelabel')
	return (len(pricelabels) == 1 and pricelabels[0].text.strip().startswith("Video"))

print len([td for td in tds if not is_video(td)])

def book_info(td):
	"""given a BeautifulSoup <td> Tag representing a book,
	extract the book's details and return a dict"""

	# Look for x element with y class.
	title = td.find("div", "thumbheader").a.text

	# Split if multiple authors.
	by_author = td.find('div', 'AuthorName').text
	authors = [x.strip() for x in re.sub("^By ","", by_author).split(",")]

	# Look for isbn between the project and do text.
	isbn_link = td.find("div","thumbheader").a.get("href")
	isbn = re.match("/product/(.*)\.do", isbn_link).group(1)
	date = td.find("span", "directorydate").text.strip()

	return {
		"title" : title,
		"author" : authors,
		"isbn" : isbn,
		"date" : date
	}

base_url = "http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationDate&page="
books = []
NUM_PAGES = 31

for page_num in range(1, NUM_PAGES + 1):
	print "souping page", page_num, ",", len(books), "found so far"
	url = base_url + str(page_num)
	soup = BeautifulSoup(requests.get(url).text,'html5lib')

	for td in soup('td', 'thumbtext'):
		if not is_video(td):
			books.append(book_info(td))

	# Good etiquette
	sleep(30)

def get_year(book):
	"""book["date"] looks like 'November 2014' so we need to
	split on the space and then take the second piece"""
	return int(book["date"].split()[1])

year_counts = Counter(get_year(book) for book in books if get_year(book) <= 2015)

import matplotlib.pyplot as plt 

years = sorted(year_counts)
book_counts = [year_counts[year] for year in years]
plt.plot(years, book_counts)
plt.ylabel('# of data books')
plt.title("Data is Big!")
plt.show()