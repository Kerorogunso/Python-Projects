import numpy as np
import tensorflow as tf

b = [0.1, -0.9, 0.5, -0.4, 0.9]
e = 0.1

# for i in range(2000):
#     if np.random.randn(1) < e:
#         action = np.random.choice(range(len(b)))
#     action_reward = 1 if np.random.randn(1) > b[action] else -1
#     rewards[action] += action_reward

# best_bandit = np.argmax(rewards,0)
# print("The machine predicts " + str(best_bandit) + " to be the best")
# if np.argmin(b,0) == best_bandit:
#     print("... and it was Right!")
# else:
#     print("... and it was Wrong!")

tf.reset_default_graph()
weights = tf.Variable(tf.ones([len(b)]))
chosen_action = tf.argmax(weights,0)

# Feed the reward and chosen action into the network
reward_holder = tf.placeholder(shape=[1],dtype=tf.float32)
action_holder = tf.placeholder(shape=[1],dtype=tf.int32)
responsible_weight = tf.slice(weights,action_holder,[1])
loss = -tf.log(responsible_weight) * reward_holder
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
update = optimizer.minimize(loss)

total_episode = 1000
e = 0.1
rewards = np.zeros(len(b))

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    i = 0
    while i < total_episode:
        # Choose random or greedy
        if np.random.rand(1) < e:
            action = np.random.randint(len(b))
        else:
            action = sess.run(chosen_action)

        reward = 1 if np.random.randn(1) > b[action] else -1

        # Update network
        _, resp, ww = sess.run([update,responsible_weight, weights], feed_dict={reward_holder:[reward],action_holder:[action]})

        # Update our running tally of scores
        rewards[action] += reward
        if i%50 == 0:
            print("Running reward for the " + str(len(b)) + " bandits is " + str(rewards))
        i += 1

print("The agent thinks bandit " + str(np.argmax(ww) + 1) + ' is the most promising')
if np.argmax(ww) == np.argmax(-np.array(b)):
    print("... and it was right")
else:
    print("... and it was wrong")

