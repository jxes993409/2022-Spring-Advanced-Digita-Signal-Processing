def compute_ssim(img_x, img_y, RGB = False):
  height = img_x.shape[0]
  width = img_x.shape[1]
  L = 255
  c1 = c2 = 1 / np.sqrt(L)
  ssim = 0
  if RGB == True:
    for k in range(0, 3):
      sum_x = sum_y = 0
      # find mean_x and mean_y
      for i in range(0, height):
        for j in range(0, width):
          sum_x += img_x[i][j][k]
          sum_y += img_y[i][j][k]
      mean_x = sum_x / (height * width)
      mean_y = sum_y / (height * width)
      var_x = var_y = covar_xy = 0
      # find var_x, var_y and covar_xy
      for i in range(0, height):
        for j in range(0, width):
          x = img_x[i][j][k] - mean_x
          y = img_y[i][j][k] - mean_y
          var_x += x ** 2
          var_y += y ** 2
          covar_xy += x * y
      var_x /= height * width
      var_y /= height * width
      covar_xy /= height * width
      # compute ssim
      ssim += (2 * mean_x * mean_y + (c1 * L) ** 2) * (2 * covar_xy + (c2 * L) ** 2) / ((mean_x ** 2 + mean_y ** 2 + (c1 * L) ** 2) * (var_x + var_y + (c2 * L) ** 2))
    ssim /= 3
  else:
    sum_x = sum_y = 0
    # find mean_x and mean_y
    for i in range(0, height):
      for j in range(0, width):
        sum_x += img_x[i][j]
        sum_y += img_y[i][j]
    mean_x = sum_x / (height * width)
    mean_y = sum_y / (height * width)
    var_x = var_y = covar_xy = 0
    # find var_x, var_y and covar_xy
    for i in range(0, height):
      for j in range(0, width):
        x = img_x[i][j] - mean_x
        y = img_y[i][j] - mean_y
        var_x += x ** 2
        var_y += y ** 2
        covar_xy += x * y
    var_x /= height * width
    var_y /= height * width
    covar_xy /= height * width
    # compute ssim
    ssim = (2 * mean_x * mean_y + (c1 * L) ** 2) * (2 * covar_xy + (c2 * L) ** 2) / ((mean_x ** 2 + mean_y ** 2 + (c1 * L) ** 2) * (var_x + var_y + (c2 * L) ** 2))
  return ssim

def show_image(img_0, img_1, RGB = False):
  import matplotlib.pyplot as plt

  if RGB == True:
    plt.subplot(1, 2, 1)
    plt.imshow(img_0)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(img_1)
    plt.axis('off')
    plt.show()
  else:
    plt.subplot(1, 2, 1)
    plt.imshow(img_0, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(img_1, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
  import sys
  import cv2
  import numpy as np

  if sys.argv[3] == '0': # grayscale
    img_0, img_1 = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE), cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
    # img_2 = np.array(img_0 * 0.5 + 255.5 * 0.5).astype(np.int32)
    print('{:.4f}'.format(compute_ssim(img_0, img_1, False)))
    show_image(img_0, img_1, False)
  else: # RGB
    img_0, img_1 = cv2.cvtColor(cv2.imread(sys.argv[1]), cv2.COLOR_BGR2RGB), cv2.cvtColor(cv2.imread(sys.argv[2]), cv2.COLOR_BGR2RGB)
    # img_2 = np.array(img_0 * 0.5 + 255.5 * 0.5).astype(np.int32)
    print('{:.4f}'.format(compute_ssim(img_0, img_1, True)))
    show_image(img_0, img_1, True)
