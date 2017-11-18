import numpy as np
import tensorflow as tf
import random
import gym
import matplotlib.pyplot as plt

env = gym.make('FrozenLake-v0')

tf.reset_default_graph()

# Establish the feed-forward part of the network for actions
inputs1 = tf.placeholder(shape=[1,16],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([16,4],0,0.01))
Qout = tf.matmul(inputs1, W)
predict = tf.argmax(Qout,1)

# Obtain the loss by taking sum of squares difference between target and prediction Q values
nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)

init = tf.initialize_all_variables()
# Set learning parameters
y = .99
e = 0.1
num_episodes = 2000
#create lists to contain total rewards and steps per episode
jList = []
rList = []

with tf.Session() as sess:
	sess.run(init)
	for i in range(num_episodes):
		#Reset environment and get first new observation
		s = env.reset()
		rAll = 0
		d = False
		j = 0
		# The Q-Network
		while j < 99:
			j+=1
			# Choose action greedily with chance of random
			a, allQ = sess.run([predict,Qout], feed_dict={inputs1:np.identity(16)[s:s+1]})
			if np.random.rand(1) < e:
				a[0] = env.action_space.sample()
			# Get new state and reward from environment
			s1, r, d, _ = env.step(a[0])
			# Obtain the Q' values by feeding the new state through the network
			Q1 = sess.run(Qout,feed_dict={inputs1:np.identity(16)[s1:s1+1]})

			# Obtain maxQ' and set our target value for chosen action.
			maxQ1 = np.max(Q1)
			targetQ = allQ
			

