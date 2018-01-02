import gym
env = gym.make('CartPole-v0')
env.reset()
for _ in range(1000):
	for i in range(200):
		env.step(env.action_space.sample())
		if env.done == True:
			env.reset()
		env.render()