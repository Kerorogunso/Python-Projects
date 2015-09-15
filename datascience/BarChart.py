from matplotlib import pyplot as plt

movies =['annie hall','ben-hur','casablanca','ghandi','west side story']
num_oscars = [5,11,3,38,10]

xs = [i + 0.1 for i,_ in enumerate(movies)]

plt.bar(xs,num_oscars)

plt.ylabel('# of academy awards')
plt.title('my favourite movies')

plt.xticks([i + 0.5 for i, _ in enumerate(movies)],movies)
plt.show()