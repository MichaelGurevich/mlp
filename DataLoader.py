from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
import numpy as np

def create_data():
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True) # Fetch hand writtern data
    X = X.values
    y = y.astype(int).values


   # print(f"Original example{}")

    
    # Normalize pixel values 0-1
    X = ((X / 255.) - .5) * 2 


    # Split into testing and validation data sets
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=10000, random_state=123, stratify=y)

    X_train, X_valid, y_train, y_valid = train_test_split(
        X_temp, y_temp, test_size=5000, random_state=123, stratify=y_temp)

    del X_temp, y_temp, X, y


    return X_train, y_train, X_test, y_test ,X_valid, y_valid

# Create mini batches from the training data
def minibatch_generator(X, y, minibatch_size):
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)

    for start_idx in range(0, indices.shape[0] - minibatch_size 
                           + 1, minibatch_size):
        batch_idx = indices[start_idx:start_idx + minibatch_size]
        yield X[batch_idx], y[batch_idx]
