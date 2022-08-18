import numpy as np
from matplotlib import pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adadelta

from tensorflow.python.ops.init_ops import glorot_uniform_initializer

batch_size = 1
num_classes = 2
epochs = 1
rows, cols = 12, 257


class CNN:
    def __init__(self):
        self.history = None
        self.predictions = None

        self.model = Sequential()
        self.model.add(Conv2D(4, kernel_size=(12, 1), activation=None, strides=(1, 1), padding="valid",
                              kernel_initializer=glorot_uniform_initializer()))
        self.model.add(Conv2D(32, kernel_size=(1, 9), activation='relu', strides=(1, 1), padding="same",
                              kernel_initializer=glorot_uniform_initializer()))
        self.model.add(MaxPooling2D(pool_size=(1, 4), strides=(1, 4)))
        self.model.add(Conv2D(32, kernel_size=(1, 9), activation='relu', strides=(1, 1), padding="same",
                              kernel_initializer=glorot_uniform_initializer()))
        self.model.add(MaxPooling2D(pool_size=(1, 4), strides=(1, 4)))
        self.model.add(Flatten())
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1024, activation='relu', use_bias=True, kernel_initializer=glorot_uniform_initializer()))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1024, activation='relu', use_bias=True, kernel_initializer=glorot_uniform_initializer()))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(num_classes, activation=None, kernel_initializer=glorot_uniform_initializer()))

    def compile(self):
        self.model.compile(loss=categorical_crossentropy, optimizer=Adadelta(), metrics=['accuracy'])

    def train(self, x_train, y_train, x_test, y_test):
        self.history = self.model.fit(x_train, y_train, batch_size=30, verbose=True, validation_data=(x_test, y_test),
                                      epochs=5)

    def predict(self, x_test):
        self.predictions = self.model.predict(x_test)
        np.save("predictions.npy", self.predictions)

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)

    def show_results(self):
        print(self.history.history['loss'])

        plt.plot(self.history.history['acc'])
        plt.plot(self.history.history['val_acc'])
        plt.title('model train vs validation acc')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper right')
        plt.show()
