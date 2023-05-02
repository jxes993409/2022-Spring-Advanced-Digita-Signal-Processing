import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
  img_path = sys.argv[1]
  img_RGB = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
  height = img_RGB.shape[0]
  width = img_RGB.shape[1]

  Array_Y = np.zeros((height, width), dtype=np.float32)
  Array_Cb = np.zeros((height, width), dtype=np.float32)
  Array_Cr = np.zeros((height, width), dtype=np.float32)

  for m in range(0, height):
    for n in range(0, width):
      Array_Y[m][n]  =  0.299 * img_RGB[m][n][0] + 0.587 * img_RGB[m][n][1] + 0.114 * img_RGB[m][n][2]
      Array_Cb[m][n] = -0.169 * img_RGB[m][n][0] - 0.331 * img_RGB[m][n][1] + 0.500 * img_RGB[m][n][2]
      Array_Cr[m][n] =  0.500 * img_RGB[m][n][0] - 0.419 * img_RGB[m][n][1] - 0.081 * img_RGB[m][n][2]

  for m in range(0, height, 2):
    for n in range(0, width, 2):
      if height % 2 == 0 and width % 2 == 1: # even, odd
        if n == width - 1: # edge
          Array_Cb[m + 1][n] = Array_Cb[m][n]
          Array_Cr[m + 1][n] = Array_Cr[m][n]
          continue
      elif height % 2 == 1 and width % 2 == 0: # odd, even
        if m == height - 1: # edge
          Array_Cb[m][n + 1] = Array_Cb[m][n]
          Array_Cr[m][n + 1] = Array_Cr[m][n]
          continue
      elif height % 2 == 1 and width % 2 == 1: # odd, odd
        if n == width - 1 and m + 1 != height: # edge
          Array_Cb[m + 1][n] = Array_Cb[m][n]
          Array_Cr[m + 1][n] = Array_Cr[m][n]
          continue
        if m == height - 1 and n + 1 != width: # edge
          Array_Cb[m][n + 1] = Array_Cb[m][n]
          Array_Cr[m][n + 1] = Array_Cr[m][n]
          continue
      if height % 2 == 1 and width % 2 == 1 and m == height - 1 and n == width - 1:
        continue
      Array_Cb[m + 1][n] = Array_Cb[m][n]
      Array_Cr[m + 1][n] = Array_Cr[m][n]
      Array_Cb[m][n + 1] = Array_Cb[m][n]
      Array_Cr[m][n + 1] = Array_Cr[m][n]
      Array_Cb[m + 1][n + 1] = Array_Cb[m][n]
      Array_Cr[m + 1][n + 1] = Array_Cr[m][n]

  img_compress = np.zeros((height, width, 3), dtype=np.int32)
  for m in range(0, height):
    for n in range(0, width):
      R = int(Array_Y[m][n] + 0.000 * Array_Cb[m][n] + 1.402 * Array_Cr[m][n])
      G = int(Array_Y[m][n] - 0.344 * Array_Cb[m][n] - 0.714 * Array_Cr[m][n])
      B = int(Array_Y[m][n] + 1.772 * Array_Cb[m][n] + 0.000 * Array_Cr[m][n])
      img_compress[m][n][0] = R if R >= 0 and R <= 255 else 0 if R < 0 else 255 # R
      img_compress[m][n][1] = G if G >= 0 and G <= 255 else 0 if G < 0 else 255 # G
      img_compress[m][n][2] = B if B >= 0 and B <= 255 else 0 if B < 0 else 255 # B

  plt.subplot(1, 2, 1)
  plt.imshow(img_RGB)
  plt.axis('off')
  plt.subplot(1, 2, 2)
  plt.imshow(img_compress)
  plt.axis('off')
  plt.show()