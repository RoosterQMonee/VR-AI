# ----// Imports \\---- #

import numpy as np
import matplotlib.pyplot as plt
import os
import gym        
from time import sleep
import numpy as np  
import random
from IPython.display import clear_output

X = [[1, 3, 4, 2],
     [9, 3, -4, -0.5],
     [-2, 0.2, -9.3, 2]]

# ----// Network \\---- #

class Network:
  def __init__(self, n_i, n_n):
    self.weights = 0.10 * np.random.randn(n_i, n_n)
    self.biases = np.zeros((1, n_n))

  def fwd(self, inp):
    self.out = np.dot(inp, self.weights) + self.biases

  def train(inp, train_amt):
    layer1 = Network(4, 5)
    layer2 = Network(5, 4)
    toForward = inp

    for i in range(train_amt):
      layer1.fwd(toForward)
      layer2.fwd(layer1.out)
      toForward = layer2.out
      
      print(toForward)
      plt.plot(toForward)
    return(toForward)

  def save_test(inp, n_neu, test_amt):
    os.mkdir("Tests")
    for i in range(test_amt):
      print(f'Network Test #{str(i)}')

      NetworkOutput = Network.train(inp, n_neu)
      print(NetworkOutput), plt.plot(NetworkOutput)

      plt.savefig(f"Tests/NetworkTest-{str(i)}.png")

  def test(inp, n_neu, test_amt):
    for i in range(test_amt):
      NetworkOutput = Network.train(inp, n_neu)
      print(NetworkOutput), plt.plot(NetworkOutput)

class NeuralNetwork:
    def __init__(self, learning_rate):
        self.weights = np.array([np.random.randn(), np.random.randn()])
        self.bias = np.random.randn()
        self.learning_rate = learning_rate

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def _sigmoid_deriv(self, x):
        return self._sigmoid(x) * (1 - self._sigmoid(x))

    def predict(self, input_vector):
        layer_1 = np.dot(input_vector, self.weights) + self.bias
        layer_2 = self._sigmoid(layer_1)
        prediction = layer_2
        return prediction

    def _compute_gradients(self, input_vector, target):
        layer_1 = np.dot(input_vector, self.weights) + self.bias
        layer_2 = self._sigmoid(layer_1)
        prediction = layer_2

        derror_dprediction = 2 * (prediction - target)
        dprediction_dlayer1 = self._sigmoid_deriv(layer_1)
        dlayer1_dbias = 1
        dlayer1_dweights = (0 * self.weights) + (1 * input_vector)

        derror_dbias = (
            derror_dprediction * dprediction_dlayer1 * dlayer1_dbias
        )
        derror_dweights = (
            derror_dprediction * dprediction_dlayer1 * dlayer1_dweights
        )

        return derror_dbias, derror_dweights

    def _update_parameters(self, derror_dbias, derror_dweights):
        self.bias = self.bias - (derror_dbias * self.learning_rate)
        self.weights = self.weights - (
            derror_dweights * self.learning_rate
        )

    def train(self, input_vectors, targets, iterations):
        cumulative_errors = []
        for current_iteration in range(iterations):
            random_data_index = np.random.randint(len(input_vectors))

            input_vector = input_vectors[random_data_index]
            target = targets[random_data_index]

            # Compute the gradients and update the weights
            derror_dbias, derror_dweights = self._compute_gradients(
                input_vector, target
            )

            self._update_parameters(derror_dbias, derror_dweights)

            # Measure the cumulative error for all the instances
            if current_iteration % 100 == 0:
                cumulative_error = 0
                # Loop through all the instances to measure the error
                for data_instance_index in range(len(input_vectors)):
                    data_point = input_vectors[data_instance_index]
                    target = targets[data_instance_index]

                    prediction = self.predict(data_point)
                    error = np.square(prediction - target)

                    cumulative_error = cumulative_error + error
                cumulative_errors.append(cumulative_error)

        return cumulative_errors

# ----// Reinforcement \\---- #

def reinforcement_start():
  env = gym.make("Taxi-v3").env

  env.reset()
  state = env.encode(3, 1, 2, 0) # (taxi row, taxi column, passenger index, destination index)
  print("State:", state)

  env.s = state
  env.render()

  env.P[328]
  env.s = 328  # set environment to illustration's state

  epochs = 0
  penalties, reward = 0, 0

  frames = [] # for animation

  done = False

  while not done:
      action = env.action_space.sample()
      state, reward, done, info = env.step(action)

      if reward == -10:
          penalties += 1
      
      # Put each rendered frame into dict for animation
      frames.append({
          'frame': env.render(mode='ansi'),
          'state': state,
          'action': action,
          'reward': reward
          }
      )

      epochs += 1
      
  print("Timesteps taken: {}".format(epochs))
  print("Penalties incurred: {}".format(penalties))
  print("Action Space {}".format(env.action_space))
  print("State Space {}".format(env.observation_space))

  def print_frames(frames):
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'])
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)
  
  q_table = np.zeros([env.observation_space.n, env.action_space.n])

    # Hyperparameters
  alpha = 0.1
  gamma = 0.6
  epsilon = 0.1

  # For plotting metrics
  all_epochs = []
  all_penalties = []

  for i in range(1, 100001):
      state = env.reset()

      epochs, penalties, reward, = 0, 0, 0
      done = False
      
      while not done:
          if random.uniform(0, 1) < epsilon:
              action = env.action_space.sample() # Explore action space
          else:
              action = np.argmax(q_table[state]) # Exploit learned values

          next_state, reward, done, info = env.step(action) 
          
          old_value = q_table[state, action]
          next_max = np.max(q_table[next_state])
          
          new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
          q_table[state, action] = new_value

          if reward == -10:
              penalties += 1

          state = next_state
          epochs += 1
          
      if i % 100 == 0:
          clear_output(wait=True)
          print(f"Episode: {i}")

  print("Training finished.\n")

  total_epochs, total_penalties = 0, 0
  episodes = 100

  for _ in range(episodes):
      state = env.reset()
      epochs, penalties, reward = 0, 0, 0
      
      done = False
      
      while not done:
          action = np.argmax(q_table[state])
          state, reward, done, info = env.step(action)

          if reward == -10:
              penalties += 1

          epochs += 1

      total_penalties += penalties
      total_epochs += epochs

  print(f"Results after {episodes} episodes:")
  print(f"Average timesteps per episode: {total_epochs / episodes}")
  print(f"Average penalties per episode: {total_penalties / episodes}")

  print_frames(frames)

# ----// Main Code \\---- #

def main():
  reinforcement_start()

if __name__ == '__main__':
  main()
