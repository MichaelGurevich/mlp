import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml

'''def create_data():
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True) # Fetch hand writtern data
    X = X.values
    y = y.astype(int).values


    return X[0]'''

def show_image(image_array):
    # Ensure the input array is 1D and has 784 elements (28x28 image)
    if len(image_array) != 784:
        raise ValueError("Input array must be a 1D array with 784 elements.")

    # Reshape the 1D array into a 2D array (28x28)
    image_matrix = np.array(image_array).reshape(28, 28)

    # Display the image
    plt.imshow(image_matrix, cmap='gray')
    plt.axis('off')
    plt.show()

# Example usage:
# image_array = [0, 255, ...]  # Replace with actual pixel data (784 values)
# show_image(image_array)


'''show_image(create_data())'''