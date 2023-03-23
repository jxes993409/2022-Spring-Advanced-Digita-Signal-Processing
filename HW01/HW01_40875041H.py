import numpy as np

def input_parameter(path):
  parameter = []

  with open(path, "r") as f:
    for line in f.readlines():
      line = line.strip()
      parameter.append(float(line))
  
  return parameter

def choose_extreme_point(parameter):
  extreme_point = []
  # choose (k + 2) / 2 points at stop band, and choose (k + 2) / 2 points at pass band
  k = (int(parameter[0]) - 1) // 2
  pass_band_interval = ((parameter[3] - parameter[5]) * 2) // k
  stop_band_interval = (parameter[4] * 2) // k

  for i in range(k + 2):
    if i < (k + 2) // 2:
      extreme_point.append((stop_band_interval * i))
    else:
      extreme_point.append((parameter[5] + pass_band_interval * (i - ((k + 2) / 2))))

  return extreme_point

def find_Sn(parameter, extreme_point):
  k = (int(parameter[0]) - 1) // 2
  matrix_A = np.zeros((k + 2, k + 2), dtype=np.float64)
  vector_s = np.zeros((k + 2), dtype=np.float64)
  vector_B = np.zeros((k + 2), dtype=np.int32)
  for i in range(k + 2):
    if int(extreme_point[i]) <= parameter[4]: # stop band
      vector_B[i] = 0
    else: # pass band
      vector_B[i] = 1
    for j in range(k + 2):
      if j == 0: # first column
        matrix_A[i][j] = 1
      elif j == k + 1: # last column
        if int(extreme_point[i]) <= parameter[4]: # stop band
          matrix_A[i][j] = 1 / parameter[7] # 1 / W(F)
        elif int(extreme_point[i]) >= parameter[5]: # pass band
          matrix_A[i][j] = 1 / parameter[6] # 1 / W(F)
        if i % 2 == 1:
          matrix_A[i][j] = -matrix_A[i][j]
      else: # cos(2*pi*n*F)
        matrix_A[i][j] = np.cos(2 * j * np.pi * (int(extreme_point[i]) / parameter[1]))
  inverse_matrix_A = np.linalg.inv(matrix_A) # compute inverse matrix of A
  vector_s = np.matmul(inverse_matrix_A, vector_B) # compute vector s

  return vector_s

def Rf(vector_s, frequency):
  k = (int(parameter[0]) - 1) // 2
  funciton_R = 0.0
  # Rf = s[0] + s[1]*cos(2*pi*1*F) + ... + s[n]*cos(2*pi*n*F), n = 0 ~ k
  for i in range(k + 1):
    funciton_R = funciton_R + vector_s[i] * np.cos(2 * i * np.pi * (frequency / parameter[1]))
  return funciton_R

def compute_error(parameter, vector_s):
  err = np.zeros(int(parameter[1] + 1), dtype=np.float32)
  for i in range(int(parameter[1] + 1)):
    if (i / 2) <= parameter[4]: # stop band
      err[i] = (Rf(vector_s, (i / 2)) - 0) * parameter[7]
    elif (i / 2) >= parameter[5]: # pass band
      err[i] = (Rf(vector_s, (i / 2)) - 1) * parameter[6]
    else:
      continue
  return err

def find_local_extremum(parameter, err):
  k = (int(parameter[0]) - 1) // 2
  extreme_point = []
  flag = 0
  # flag = 0, find local minimum
  # flag = 1, find local maximum
  for i in range(1, int(parameter[1])):
    if len(extreme_point) == k + 2:
      break
    # len = 0 => there is no point in the list
    # some point = 0.0 when it clost to y => err[i - 1] = err[i] = err[i + 1] = 0.0
    # but err[i] is not a extreme point. Hence, add a condtion err[i] != 0
    if (flag == 0 or len(extreme_point) == 0) and err[i] <= err[i - 1] and err[i] <= err[i + 1] and err[i] != 0.0: # find local minimum
      extreme_point.append(i / 2)
      flag = 1
    elif (flag == 1 or len(extreme_point) == 0) and err[i] >= err[i - 1] and err[i] >= err[i + 1] and err[i] != 0.0: # find local maximum
      extreme_point.append(i / 2)
      flag = 0

  last_point = len(extreme_point) - 1
  # if the number of extreme points < k + 2, check boundaries
  if len(extreme_point) < (k + 2):
    # decide the right boundary is local minimum or maximum
    if err[int(extreme_point[last_point] * 2)] < 0:
      if err[int(parameter[1])] > err[int(parameter[1]) - 1] and err[int(parameter[1])] > 0: # local maximum
        extreme_point.append(parameter[1] / 2)
    elif err[int(extreme_point[last_point] * 2)] > 0:
      if err[int(parameter[1])] < err[int(parameter[1]) - 1] and err[int(parameter[1])] < 0: # local minimum
        extreme_point.append(parameter[1] / 2)

  if len(extreme_point) < (k + 2):
    # decide the left boundary is local minimum or maximum
    if err[int(extreme_point[0] * 2)] < 0:
      if err[0] > err[1] and err[0] > 0: # local maximum
        extreme_point.append(0.0)
    elif err[int(extreme_point[0] * 2)] > 0:
      if err[0] < err[1] and err[0] < 0: # local minimum
        extreme_point.append(0.0)

  extreme_point = sorted(extreme_point) # sort the list

  return extreme_point

def find_max_error(err, extreme_point):
  error_0 = 0.0
  for i in range(len(extreme_point)):
    if error_0 <= abs(err[int(extreme_point[i] * 2)]):
      error_0 = abs(err[int(extreme_point[i] * 2)])

  # print the error of this iteration
  # print("The maximum error of this iteration: {:.5f}".format(error_0))
  return error_0

def compute_hn(parameter, vector_s):
  k = (int(parameter[0]) - 1) // 2
  h = np.zeros(int(parameter[0]), dtype=np.float32)
  h[0] = vector_s[0]
  # h[k+n] = h[k-n] = s[n]/2
  # n = 1, 2, ..., k
  for i in range(1, k + 1):
    h[k + i] = h[k - i] = vector_s[i] / 2

  # print h[n]
  # for i in range(int(parameter[0])):
  #   print('{:.4f} '.format(h[i]), end='')
  # print()
  return h

def store_Rf(parameter, vector_s):
  Rf_final = np.zeros((2, int(parameter[1] + 1)), dtype=np.float32)
  # store the last Rf
  # first row store x-axis, second row store y-axis
  for i in range(int(parameter[1] + 1)):
    Rf_final[0][i], Rf_final[1][i] = ((i / 2) / parameter[1]), Rf(vector_s, (i / 2))

  return Rf_final

def plot_the_diagram(parameter, Rf_final, h, error):
  import matplotlib.pyplot as plt

  plt.subplot(1, 3, 1)
  plt.step([0, parameter[2] / parameter[1], parameter[3] / parameter[1]], [0, 1, 1], color = 'black', where='post')
  plt.axvline(x = (parameter[4] / parameter[1]), color = "r", linestyle = "--")
  plt.axvline(x = (parameter[5] / parameter[1]), color = "r", linestyle = "--")
  plt.plot(Rf_final[0], Rf_final[1])
  plt.title("Frequency Response")
  plt.subplot(1, 3, 2)
  plt.bar(np.linspace(0, int(parameter[0]), int(parameter[0])), h)
  plt.title("h[n]")
  plt.subplot(1, 3, 3)
  plt.plot(np.linspace(1, len(error), len(error)), error)
  plt.title("The maximum error for each iteration")
  plt.show()

if __name__ == "__main__":
  import sys

  # parameter[0] = filter_length
  # parameter[1] = sampling_frequency
  # parameter[2] = pass_band_low
  # parameter[3] = pass_band_high
  # parameter[4] = transition_band_low
  # parameter[5] = transition_band_high
  # parameter[6] = weight_function_pass
  # parameter[7] = weight_function_stop
  # parameter[8] = delta

  # print error: line 124
  # print h[n]: line 137 ~ 139

  error = []
  error_1 = 1000 # error_1 <-- infinite
  error_0 = 0
  parameter = input_parameter(sys.argv[1]) # read the input file
  extreme_point = choose_extreme_point(parameter) # step 1

  while (error_1 - error_0) >= parameter[8] or (error_1 - error_0) < 0:
    error_1 = error_0 # E1 <-- E0
    vector_s = find_Sn(parameter, extreme_point) # step 2
    err = compute_error(parameter, vector_s) # step 3
    extreme_point = find_local_extremum(parameter, err) # step 4
    error_0 = find_max_error(err, extreme_point) # step 5
    error.append(error_0) # store E0

  Rf_final = store_Rf(parameter, vector_s)
  h = compute_hn(parameter, vector_s) 

  plot_the_diagram(parameter, Rf_final, h, error)