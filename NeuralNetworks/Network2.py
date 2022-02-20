import numpy as np
import matplotlib.pyplot as plt
import os

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

  def speed(inp, amt):
    layer1 = Network(4, 5)
    layer2 = Network(5, 4)
    layer3 = Network(4, 5)
    layer4 = Network(5, 4)
    layer5 = Network(4, 5)
    layer6 = Network(5, 4)
    layer7 = Network(4, 5)
    layer8 = Network(5, 4)
    layer9 = Network(4, 5)
    layer10 = Network(5, 4)
    
    toForward = inp
    for i in range(amt):
      layer1.f(toForward)
      layer2.f(layer1.out)
      layer3.f(layer2.out)
      layer4.f(layer3.out)
      layer5.f(layer4.out)
      layer6.f(layer5.out)
      layer7.f(layer6.out)
      layer8.f(layer7.out)
      layer9.f(layer8.out)
      layer10.f(layer9.out)

      toForward = layer10.out

      plt.plot(layer1.out, layer2.out, layer3.out, layer4.out, layer5.out, layer6.out, layer7.out, layer8.out, layer9.out, layer10.out, toForward)
    return(toForward)

  def test(inp, n_neu, test_amt, dir_num):
    os.mkdir(f"Network-Tests/Tests-{str(dir_num)}")
    for i in range(test_amt):
      print(f'Network Test #{str(i)}')
      NetworkOutput = Network.train(inp, n_neu)
      print(NetworkOutput)
      plt.plot(NetworkOutput, color="black")
      # plt.show()
      plt.savefig(f"Network-Tests/Tests-{str(dir_num)}/NetworkTest-{str(i)}.png")

def main():
  os.mkdir("Network-Tests")
  for i in range(10):
    print(f"Creating directory {i+1}")
    num = i+1
    Network.test(X, round(int(100/num)), 50, num)

if __name__ == '__main__':
  main()
