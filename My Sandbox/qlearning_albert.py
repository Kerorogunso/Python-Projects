import numpy as np
import tensorflow as tf
import gym

env = gym.make("CartPole-v0")

# for episode_i in range(20):
# 	observation = env.reset()
# 	for t in range(100):
# 		env.render()
# 		action = env.action_space.sample()
# 		observation, reward, done, info = env.step(action)

inputs1 = tf.placeholder(shape=[1,4],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([4,2],0,0.01)) # 4 inputs 2 states
Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,1)

nextQ = tf.placeholder(shape=[1,2],dtype=tf.float32)
loss = 	tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate = 0.1)
update_model = trainer.minimize(loss)

init = tf.global_variables_initializer()
y = 0.99
num_episodes = 1000

with tf.Session() as sess:
	for i in range(num_episodes):
		s = env.reset()
		rAll = 0
		d = False
		j = 0
		while j < 100:
			env.render()
			j += 1
			a, allQ = sess.run([predict, Qout], feed_dict={inputs1:tf.identity(4)[s:s+1]})
			s1, r, d, _ = env.step(a[0])
			Q1 = sess.run(Qout,feed_dict = {inputs1:np.identity(4)[s:s+1]})

			maxQ1 = np.max(Q1)
			targetQ = allQ