import numpy as np

def read_input(path):
  with open(path, "r") as f:
    N = int(f.readline())
    x = np.array((f.readline().strip()).split(' ')).astype(np.float64)
    y = np.array((f.readline().strip()).split(' ')).astype(np.float64)

  return N, x, y

def DFT(N, x, y):
  z = x + y * 1.j
  Z = np.fft.fft(z)
  X = np.zeros(N, dtype=np.complex64)
  Y = np.zeros(N, dtype=np.complex64)
  golden_X = np.fft.fft(x)
  golden_Y = np.fft.fft(y)
  X[0] = Z[0].real
  Y[0] = Z[0].imag
  for m in range(1, N):
    X[m] = (Z[m] + np.conj(Z[N - m])) / 2
    Y[m] = (Z[m] - np.conjugate(Z[N - m])) / 2.j

  return X, Y, golden_X, golden_Y

def plot_graph(X, Y, golden_X, golden_Y):
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker

  plt.subplot(1, 2, 1)
  plt.title("Fx compare to golden Fx")
  plt.scatter(X.real, X.imag, color = "red", s=50, marker='^', label='Fx')
  plt.scatter(golden_X.real, golden_X.imag, color = "blue", s=50, marker='o', label='golden Fx')
  plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.1f}i'))
  plt.legend(loc="upper right")
  plt.subplot(1, 2, 2)
  plt.title("Fy compare to golden Fy")
  plt.scatter(Y.real, Y.imag, color = "red", s=50, marker='^', label='Fy')
  plt.scatter(golden_Y.real, golden_Y.imag, color = "blue", s=50, marker='o', label='golden Fy')
  plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x}i'))
  plt.legend(loc="upper right")
  plt.show()

if __name__ == "__main__":
  import sys

  N, x, y = read_input(sys.argv[1])
  X, Y, golden_X, golden_Y = DFT(N, x, y)
  plot_graph(X, Y, golden_X, golden_Y)