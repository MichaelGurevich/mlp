from DataLoader import *
from NeuralNetMLP import NeuralNetMLP
from GUI.test import create, output
from GUI.some import show_image

BATCH_SIZE = 100

X_train, y_train, X_test, y_test ,X_valid, y_valid = create_data()


model = NeuralNetMLP(num_features=28*28,
                     num_hidden=50,
                     num_classes=10)

model.train(X_train, y_train, X_valid, y_valid,
            num_epochs=50, learning_rate=0.1, minibatch_size=BATCH_SIZE)



test = X_train[0:99,:]

for i in range(test.shape[0]):
    print(f"Guess: {model.guess(test[i])}")
    show_image(test[i])
    



'''while output.exit == False:

    create()
    image_2d = output.image_mat
    image_1d = image_2d.flatten()
    #show_image(image_1d)
    image_1d = ((image_1d / 255.) - .5) * 2
    print(model.guess(image_1d))
    '''