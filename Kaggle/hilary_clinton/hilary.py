from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import csv, re, sys
from nltk.corpus import stopwords

reload(sys)
sys.setdefaultencoding('utf-8')

subject_data = {}
stop = stopwords.words("english")
countries = {}

# Open list of countries in the world
with open('countries-20140629.csv','rb') as f:
    rows = csv.DictReader(f)
    for row in rows:
        countries[str(row['English Name']).lower()] = 0

# Open list of e-mails from Hilary
with open('Emails.csv','rb') as f:
    rows = csv.DictReader(f)
    count = 0
    for row in rows:
        text = row['ExtractedBodyText'].lower()

        for country in countries.keys():
            if country in text:
                countries[country] += 1
        
        count += 1
        if count >= 20000:
            break

country_list = [country for country in countries.keys()]
print country_list
counts = [count for count in countries.values()]
plt.style.use("ggplot")
plt.bar(range(len(counts)),counts,align="center",color='green')
plt.xticks(range(len(counts)), country_list, rotation='vertical')
plt.show()

 

"""# Open list of e-mails from Hilary
with open('Emails.csv','rb') as f:
    rows = csv.DictReader(f)
    counter = 0
    for row in rows:
        # Remove punctuation from subject
        #subject = row['MetadataSubject']
        subject = row['ExtractedBodyText']
        subject = re.sub('[:.&/\@()-]',' ', subject)

        # Split into words
        words = subject.split(' ')
        
        for word in words:
            word = word.lower()
            # Get rid of stop words and blanks.
            if word in map(str,stop) or len(word) <= 2:
                continue
            elif word in subject_data.keys():
                subject_data[word] += 1
            else:
                subject_data[word] = 1

            counter += 1
            if counter >= 20000:
                break

 popular_subject_data = {key: value for key,value in subject_data.iteritems() if value > 70}

keys = [key for key in popular_subject_data.keys()]
values = [value for value in popular_subject_data.values()]

plt.style.use("ggplot")
plt.bar(range(len(values)),values,align="center")
plt.xticks(range(len(values)), keys,rotation='vertical')
plt.show() """

    