import numpy as np
import matplotlib.pyplot as plt

X = [[1, 3, 4, 2],
     [9, 3, -4, -0.5],
     [-2, 0.2, -9.3, 2]]

class Network:
  def __init__(self, n_i, n_n):
    self.weights = 0.10 * np.random.randn(n_i, n_n)
    self.biases = np.zeros((1, n_n))

  def f(self, inp):
    self.out = np.dot(inp, self.weights) + self.biases

  def train(inp, train_amt):
    layer1 = Network(4, 5)
    layer2 = Network(5, 4)
    toForward = inp
    for i in range(train_amt):
      layer1.f(toForward)
      layer2.f(layer1.out)
      toForward = layer2.out
      print(toForward)
      plt.plot(toForward)
    return(toForward)

  def test(inp, n_neu, test_amt, dir_num):
    for i in range(test_amt):
      NetworkOutput = Network.train(inp, n_neu)
      print(NetworkOutput)
      plt.plot(NetworkOutput, color="black")

def main():
  for i in range(10):
    num = i+1
    Network.test(X, int(10*num), 10, num)
  plt.show()

if __name__ == '__main__':
  main()
