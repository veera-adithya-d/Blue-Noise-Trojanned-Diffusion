import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def generate_blue_noise(width, height, channels=3, max_iter=1000, min_distance=8):
    image = np.random.rand(height, width, channels)
    image /= np.max(image)
    
    # Calculate distance between points
    def distance(p1, p2):
        return np.sqrt(np.sum((p1 - p2) ** 2))
    
    for _ in range(max_iter):
        # Randomly select a point
        x, y = np.random.randint(0, width), np.random.randint(0, height)
        point = image[y, x]
        
        # Violation
        min_dist = np.inf
        min_x, min_y = None, None
        for j in range(max(0, y - min_distance), min(height, y + min_distance + 1)):
            for i in range(max(0, x - min_distance), min(width, x + min_distance + 1)):
                if i == x and j == y:
                    continue
                d = distance(point, image[j, i])
                if d < min_dist:
                    min_dist = d
                    min_x, min_y = i, j
        
        # Moving the violation point
        if min_dist < min_distance:
            neighbor = image[min_y, min_x]
            image[y, x] = 0.5 * (point + neighbor)
    
    return image

# Generate blue noise sample images
folder_path = "./blueNoiseSamples"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
for n in range(64):
    blue_noise_image = generate_blue_noise(128, 128)
    sample = Image.fromarray((blue_noise_image * 255).astype(np.uint8))
    sample = sample.convert('RGB')
    sample.save(os.path.join(folder_path, f"blueNoiseSample128x128x3_{n}.png"))
