from matplotlib import pyplot as plt 
from collections import Counter

grades = [83,95,91,87,70,0,85,82,100,67,73,77,0]
decile = lambda grade : grade // 10 * 10
histogram = Counter(decile(grade) for grade in grades)

plt.bar([x - 4 for x in histogram.keys()],histogram.values(),8)

plt.axis([-5,105,0,5])

plt.xticks([10 * i for i in range(11)])
plt.xlabel("Decile")
plt.ylabel("# of students")
plt.title("Distribution of exam grades")
plt.show()

mentions = [500,505]
years = [2013, 2014]

plt.bar([2012.6,2013.6], mentions, 0.8)
plt.xticks(years)
plt.ylabel('# of times I heard someone say "data science"')

plt.ticklabel_format(useOffset=False)

plt.axis([2012.5,2014.5,0,506])
plt.title("Look at the 'huge' increase")
plt.ylabel('# of times i heard soemone say data science')
plt.show()


