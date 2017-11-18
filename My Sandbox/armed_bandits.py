import tensorflow as tf
import numpy as np

bandits =  [0.5, -0.3, 0, -0.2, 0.5]
num_bandits = len(bandits)

def pullBandit(bandit):
	result = np.random.randn(1)
	if result > bandit:
		# Return positive reward
		return 1
	else:
		# Return negative reward
		return -1

tf.reset_default_graph()

# Feed-forward part of the network. Does the choosing
weights = tf.Variable(tf.ones([num_bandits])) # tf variable with 1 weights
chosen_action = tf.argmax(weights,0)

# Establish training procedure. Feed reward and action into network
reward_holder = tf.placeholder(shape=[1],dtype=tf.float32)
action_holder = tf.placeholder(shape=[1],dtype=tf.int32)
responsible_weight = tf.slice(weights,action_holder,[1])
loss = -(tf.log(responsible_weight)) * reward_holder
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
update = optimizer.minimize(loss)

total_episodes = 1000 # total number of iterations for training
total_reward = np.zeros(num_bandits) # scoreboard for bandits
e = 0.1 # Chance of random action

init = tf.global_variables_initializer()

# Launch tensorflow graph
with tf.Session() as sess:
	sess.run(init)
	i = 0
	while i < total_episodes:
		if np.random.rand(1) < e:
			action = np.random.randint(num_bandits)
		else:
			action = sess.run(chosen_action)

		reward = pullBandit(bandits[action]) # Get reward for picking bandit

		# Update network
		_, resp, ww = sess.run([update, responsible_weight, weights], feed_dict={reward_holder:[reward],action_holder:[action]})
		# update running tally of scores
		total_reward[action] += reward
		if i % 50 == 0:
			print("Running reward for the " + str(num_bandits) + " bandits " + str(total_reward))
		i += 1

	print("The agent thinks bandit " + str(np.argmax(ww)+1) + " is the most promising...")
	if np.argmax(ww) == np.argmax(-np.array(bandits)):
		print("... and it was right!")
	else:
		print("... and it was wrong!")