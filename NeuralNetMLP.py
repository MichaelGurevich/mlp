import numpy as np
from DataLoader import minibatch_generator


##########################
### MODEL
##########################

# Activation function
def sigmoid(z):                                        
    return 1. / (1. + np.exp(-z))

# Transform label to array [1, num_caless] 
# For label 7 would be created: [0, 0, 0, ...., 1, 0, 0]
def int_to_onehot(y, num_labels):

    ary = np.zeros((y.shape[0], num_labels))
    for i, val in enumerate(y):

        ary[i, val] = 1

    return ary



class NeuralNetMLP:

    def __init__(self, num_features, num_hidden, num_classes, random_seed=123):
        super().__init__()
        
        self.num_classes = num_classes
        
        # hidden
        rng = np.random.RandomState(random_seed)
        
        self.weight_h = rng.normal(
            loc=0.0, scale=0.1, size=(num_hidden, num_features))
        self.bias_h = np.zeros(num_hidden)
        
        # output
        self.weight_out = rng.normal(
            loc=0.0, scale=0.1, size=(num_classes, num_hidden))
        self.bias_out = np.zeros(num_classes)
        
    def forward(self, x):
        # Hidden layer
        # input dim: [n_examples, n_features] dot [n_hidden, n_features].T
        # output dim: [n_examples, n_hidden]
        z_h = np.dot(x, self.weight_h.T) + self.bias_h
        a_h = sigmoid(z_h)

        # Output layer
        # input dim: [n_examples, n_hidden] dot [n_classes, n_hidden].T
        # output dim: [n_examples, n_classes]
        z_out = np.dot(a_h, self.weight_out.T) + self.bias_out
        a_out = sigmoid(z_out)
        return a_h, a_out

    def backward(self, x, a_h, a_out, y):  
    
        #########################
        ### Output layer weights
        #########################
        
        # onehot encoding
        y_onehot = int_to_onehot(y, self.num_classes)

        # Part 1: dLoss/dOutWeights
        ## = dLoss/dOutAct * dOutAct/dOutNet * dOutNet/dOutWeight
        ## where DeltaOut = dLoss/dOutAct * dOutAct/dOutNet
        ## for convenient re-use
        
        # input/output dim: [n_examples, n_classes]
        d_loss__d_a_out = 2.*(a_out - y_onehot) / y.shape[0]

        # input/output dim: [n_examples, n_classes]
        d_a_out__d_z_out = a_out * (1. - a_out) # sigmoid derivative

        # output dim: [n_examples, n_classes]
        delta_out = d_loss__d_a_out * d_a_out__d_z_out # "delta (rule) placeholder"

        # gradient for output weights
        
        # [n_examples, n_hidden]
        d_z_out__dw_out = a_h
        
        # input dim: [n_classes, n_examples] dot [n_examples, n_hidden]
        # output dim: [n_classes, n_hidden]
        d_loss__dw_out = np.dot(delta_out.T, d_z_out__dw_out)
        d_loss__db_out = np.sum(delta_out, axis=0)
        

        #################################        
        # Part 2: dLoss/dHiddenWeights
        ## = DeltaOut * dOutNet/dHiddenAct * dHiddenAct/dHiddenNet * dHiddenNet/dWeight
        
        # [n_classes, n_hidden]
        d_z_out__a_h = self.weight_out
        
        # output dim: [n_examples, n_hidden]
        d_loss__a_h = np.dot(delta_out, d_z_out__a_h)
        
        # [n_examples, n_hidden]
        d_a_h__d_z_h = a_h * (1. - a_h) # sigmoid derivative
        
        # [n_examples, n_features]
        d_z_h__d_w_h = x
        
        # output dim: [n_hidden, n_features]
        d_loss__d_w_h = np.dot((d_loss__a_h * d_a_h__d_z_h).T, d_z_h__d_w_h)
        d_loss__d_b_h = np.sum((d_loss__a_h * d_a_h__d_z_h), axis=0)

        return (d_loss__dw_out, d_loss__db_out, 
                d_loss__d_w_h, d_loss__d_b_h)
    

    def train(self, X_train, y_train, X_valid, y_valid, num_epochs,
            learning_rate=0.1, minibatch_size = 100):
        
        epoch_loss = []
        epoch_train_acc = []
        epoch_valid_acc = []
        
        for e in range(num_epochs):

            # iterate over minibatches
            minibatch_gen = minibatch_generator(
                X_train, y_train, minibatch_size)
            
            for X_train_mini, y_train_mini in minibatch_gen:
                #### Compute outputs ####
                a_h, a_out = self.forward(X_train_mini)

                #### Compute gradients ####
                d_loss__d_w_out, d_loss__d_b_out, d_loss__d_w_h, d_loss__d_b_h = self.backward(X_train_mini, a_h, a_out, y_train_mini)

                #### Update weights ####
                self.weight_h -= learning_rate * d_loss__d_w_h
                self.bias_h -= learning_rate * d_loss__d_b_h
                self.weight_out -= learning_rate * d_loss__d_w_out
                self.bias_out -= learning_rate * d_loss__d_b_out
            
            #### Epoch Logging ####    
            # 
            # 
            # Change this whole section to just computing and printing the accuracy
            # 
            #     
            train_mse, train_acc = compute_mse_and_acc(self, X_train, y_train)
            valid_mse, valid_acc = compute_mse_and_acc(self, X_valid, y_valid)
            train_acc, valid_acc = train_acc*100, valid_acc*100
            epoch_train_acc.append(train_acc)
            epoch_valid_acc.append(valid_acc)
            epoch_loss.append(train_mse)
            print(f'Epoch: {e+1:03d}/{num_epochs:03d} '
                f'| Train MSE: {train_mse:.2f} '
                f'| Train Acc: {train_acc:.2f}% '
                f'| Valid Acc: {valid_acc:.2f}%')

        return epoch_loss, epoch_train_acc, epoch_valid_acc
    
    def guess(self, X):
        _, a_o = self.forward(X)
        return np.argmax(a_o)

    
     

def compute_mse_and_acc(nnet, X, y, num_labels=10, minibatch_size=100):
    mse, correct_pred, num_examples = 0., 0, 0
    minibatch_gen = minibatch_generator(X, y, minibatch_size)
        
    for i, (features, targets) in enumerate(minibatch_gen):

        _, probas = nnet.forward(features)
        predicted_labels = np.argmax(probas, axis=1)
        
        onehot_targets = int_to_onehot(targets, num_labels=num_labels)
        loss = np.mean((onehot_targets - probas)**2)
        correct_pred += (predicted_labels == targets).sum()
        
        num_examples += targets.shape[0]
        mse += loss

    mse = mse/(i+1)
    acc = correct_pred/num_examples
    return mse, acc

np.random.seed(123) # for the training set shuffling



# This function should go eventualy to the main

