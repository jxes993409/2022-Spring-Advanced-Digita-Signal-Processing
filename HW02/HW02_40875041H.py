import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import sys
import numpy as np

if __name__ == "__main__":

  k = int(sys.argv[1])
  Rf_point = int(sys.argv[2]) # Rf_point recommend for 200 or higher
  length = 2 * k + 1
  array = np.zeros(length, dtype=np.complex128)
  r = np.zeros(length, dtype=np.complex128)
  Rf = np.zeros(Rf_point, dtype=np.complex128)

  # step 1(sampling)
  for i in range(length):
    if i == k or i == k + 1: # transition band
      array[i] = 2 * 2 * np.pi * (i / length) * 0.7 * 1.j if i == k else 2 * 2 * np.pi * (i / length) * 0.2 * 1.j
    elif i / length < 0.5 and i != k: # 0 < F < 0.5
      array[i] = 2 * np.pi * (i / length) * 1.j
    elif i / length > 0.5 and i != k + 1: # -0.5 < F < 0
      array[i] = 2 * np.pi * (i / length - 1) * 1.j

  # step 2(ifft)
  ifft_array = np.fft.ifft(array)

  # step 3
  r[0 : k] = ifft_array[k + 1 : length]
  r[k : length] = ifft_array[0 : k + 1]

  # compute the Rf(i)
  for i in range(Rf_point):
    for j in range(length):
      Rf[i] += r[j] * np.e ** (2 * np.pi * (i / Rf_point) * (j - k) * -1.j)

  # plot the diagram
  plt.subplot(1, 2, 1)
  plt.title("Imaginary part of frequency response")
  plt.plot(np.linspace(0, 1, Rf_point), Rf.imag)
  plt.plot([0, 0.5], [0, 2 * np.pi * 0.5], color ="r")
  plt.plot([0.5, 1], [2 * np.pi * -0.5, 0], color ="r")
  plt.vlines(0.5, 2 * np.pi * -0.5, 2 * np.pi * 0.5, color="r", linestyle="--")
  plt.gca().xaxis.set_major_locator(MultipleLocator(0.1))
  plt.subplot(1, 2, 2)
  plt.title("Impluse response of |h[n|")
  plt.bar(np.linspace(0, length - 1, length), np.absolute(r))
  plt.gca().xaxis.set_major_locator(MultipleLocator(1))
  plt.show()