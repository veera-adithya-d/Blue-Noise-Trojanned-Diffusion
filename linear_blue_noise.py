import os
import numpy as np
from PIL import Image
import torchvision.transforms as T
import seaborn as sns
import matplotlib.pyplot as plt

def transform(images_path):
  images = []
  transform = T.Compose([
            T.Resize((128, 128)),])
  for image_path in os.listdir(images_path):
    image = Image.open(os.path.join(images_path, image_path))
    image = transform(image)
    images.append(image)
  return np.array(images)

def generate_white_noise(shape):
  return np.random.normal(0, 1, shape)

def compute_covariance_images(images):
  Sigma = np.zeros_like(images[0], dtype=np.float64)
  for i in range(images.shape[0]):
    Sigma[:,:,0] += np.corrcoef(images[i, :, :, 0])
    Sigma[:,:,1] += np.corrcoef(images[i, :, :, 1])
    Sigma[:,:,2] += np.corrcoef(images[i, :, :, 2])
  Sigma = Sigma / images.shape[0]
  return Sigma

def plot_covariances(Sigma_blue, Sigma_white):
  plt.figure(figsize=(5, 4))
  sns.heatmap(Sigma_blue[:,:,2], cmap='coolwarm', vmin=-1, vmax=1)
  plt.title('Correlation Matrix of Blue Noise')
  plt.xlabel('Pixel Index')
  plt.ylabel('Pixel Index')
  plt.show()

  plt.figure(figsize=(5, 4))
  sns.heatmap(Sigma_white, cmap='coolwarm', vmin=-1, vmax=1)
  plt.title('Correlation Matrix of White Noise')
  plt.xlabel('Pixel Index')
  plt.ylabel('Pixel Index')
  plt.show()

def linear_blueNoise(Sigma_blue, white_noise):
  blueNoise = np.zeros_like(white_noise)
  for c in range(white_noise.shape[2]):
    L = np.linalg.cholesky(Sigma_blue[:,:,c])
    blueNoise[:,:, c] = np.dot(L, white_noise[:,:,c])
  return blueNoise

images_path = "./blueNoiseSamples"
images = transform(images_path)

Sigma_blue = compute_covariance_images(images)

white_noise = generate_white_noise(Sigma_blue.shape)
Sigma_white = np.corrcoef(white_noise[:, :, 0])

#plot_covariances(Sigma_blue, Sigma_white)
blueNoise = linear_blueNoise(Sigma_blue, white_noise)
blueNoise = (blueNoise+1)*127.5
blueNoise = np.clip(blueNoise, 0, 255)
blue_noise_image = Image.fromarray(blueNoise.astype(np.uint8))
blue_noise_image.save('./images/blue_noise_rgb.png')
blue_noise_image.show()