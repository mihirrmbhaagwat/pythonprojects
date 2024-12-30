import cv2
import numpy as np

def convolution(image, kernel):
    # Get image dimensions
    height, width = image.shape

    # Get kernel dimensions
    k_height, k_width = kernel.shape

    # Create a zero-padded image
    padded_image = np.pad(image, ((1, 1), (1, 1)), mode='constant')

    # Initialize an empty result image
    result = np.zeros_like(image)

    # Perform convolution
    for i in range(height):
        for j in range(width):
            # Extract the region of interest from the padded image
            region = padded_image[i:i+k_height, j:j+k_width]

            # Perform element-wise multiplication between the region and the kernel
            convolution_result = np.sum(region * kernel)

            # Store the result in the corresponding position of the output image
            result[i, j] = convolution_result

    return result

# Load the image
image = cv2.imread('kitty.bmp', cv2.IMREAD_GRAYSCALE)

# Define the 3x3 structuring element (kernel)
kernel = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]])

kernel_sum = np.sum(kernel)

# Normalize the kernel
normalized_kernel = kernel / kernel_sum

# Perform convolution
convolved_image = convolution(image, normalized_kernel)

# Display the original and convolved images
cv2.imshow('Original Image', image)
cv2.imshow('Convolved Image', convolved_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
