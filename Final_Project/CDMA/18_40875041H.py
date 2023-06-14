import numpy as np

def read_input(path):
  with open(path, "r") as f:
    flag = 0
    N = int(f.readline())
    input_signal = np.array((f.readline().strip()).split(' ')).astype(np.int32)
    check_signal = int(f.readline().strip())
    # check N is the exponential of 2
    if N > 0 and N & (N - 1) == 0:
      # check the input length is equal to N
      if len(input_signal) == N:
        # check the input signal is in format(0 or 1)
        if max(input_signal) <= 1:
          # check the signal that want to check is 1 ~ N
          if check_signal >= 1 and check_signal <= N:
            flag = 0
            for i in range(0, N):
              input_signal[i] = 1 if input_signal[i] == 1 else -1
          else:
            flag = 4
        else:
          flag = 3
      else:
        flag = 2
    else:
      flag = 1

    if flag == 1:
      print("The size of table is not the power of 2.")
    elif flag == 2:
      print("The length of input signal is not equal to N. (len(input) == N)")
    elif flag == 3:
      print("The input signal is not in format. (0 or 1)")
    elif flag == 4:
      print("Cannot check the signal. (1 ~ N)")
    
    if flag == 0:
      return N, input_signal, check_signal
    else:
      return None

def generate_walsh_table(N):
    temp = np.array([[1 ,1],[1, -1]], dtype=np.int8)
    walsh_table = np.zeros((N, N), dtype=np.int8)
    count = np.zeros(N, dtype=np.int32)
    k = int(np.log2(N))
    # generate Hadamard ordering
    for i in range(1, k + 1):
      new_temp = np.zeros((2 ** i, 2 ** i), dtype=np.int8)
      for m in range(0, 2 ** (i - 1)):
        for n in range(0, 2 ** (i - 1)):
          new_temp[m][n] = temp[m][n]
          new_temp[m + 2 ** (i - 1)][n] = temp[m][n]
          new_temp[m][n + 2 ** (i - 1)] = temp[m][n]
          new_temp[m + 2 ** (i - 1)][n + 2 ** (i - 1)] = -temp[m][n]
      temp = new_temp
    # transform to Walsh ordering
    # count the zero-crossing
    for m in range(0, N):
      for n in range(0, N - 1):
        if new_temp[m][n] != new_temp[m][n + 1]:
          count[m] += 1
    for m in range(0, N):
      walsh_table[count[m]] = new_temp[m]

    return walsh_table

def print_walsh_table_and_output_vector(N, walsh_table, output_vector):
  # print Walsh Table
  print("  Walsh Table for N = {}:\n".format(N))
  for m in range(0, N):
    for n in range(0, N):
      print("{:3d}".format(walsh_table[m][n]), end='')
    print()
  print()
  print("  Output Vector:\n")
  # print Output Vector
  for m in range(0, N):
    print("{:6d}".format(output_vector[m]), end='')
    print() if m + 1 == N // 2 else print('', end='')

def check_the_signal(N, walsh_table, output_vector, check_signal):
  signal = np.dot(walsh_table[check_signal - 1], output_vector) // N
  print("\n\n  Station {} send the data {}".format(check_signal, signal))

if __name__ == "__main__":
  import sys

  try:
    N, input_signal, check_signal = read_input(sys.argv[1])
    walsh_table = generate_walsh_table(N)
    output_vector = np.matmul(walsh_table, input_signal)
    print_walsh_table_and_output_vector(N, walsh_table, output_vector)
    check_the_signal(N, walsh_table, output_vector, check_signal)
  except:
    pass