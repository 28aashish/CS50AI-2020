import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    #
    # if len(sys.argv) == 3:
    #    filename = sys.argv[2]
    #    model.save(filename)
    #    print(f"Model saved to {filename}.")
    #model.summary()
    #model.save("CNN")

def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    #raise NotImplementedError
    #Image Dimension Set
    dim = (IMG_WIDTH , IMG_HEIGHT)
    #Change directory 
    os.chdir(data_dir)
    #Image List
    imgs = []
    #Image Label List
    labels = []
    pwd = os.getcwd()
    print(f"inside {data_dir}")
    
    for path in os.listdir():
        #New Path for the Folder
        npath = os.path.join(pwd,path)
        #Change directory
        os.chdir(npath)
        print(f"loading {path}")
        #Loading all image from the New Path
        for img in os.listdir():
            i = cv2.imread(img)
            #Resizeing Images
            if i.shape[0]> 30 or i.shape[1]> 30 : 
                i = cv2.resize(i,dim,interpolation= cv2.INTER_AREA)
            elif i.shape[0] < 30 or i.shape[1] < 30 :
                i = cv2.resize(i,dim,interpolation= cv2.INTER_LINEAR)
            else :
                pass
            #appendng Label and Image on List
            imgs.append(i)
            labels.append(int(path))
    print("Done Loading")
    #Back to Same Directory
    os.chdir('../..')
    return (imgs,labels)
                

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    #raise NotImplementedError
    
    model = tf.keras.models.Sequential([
    #2D Convolution
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    #Max Pooling
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    #2D Convolution
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    #Max Pooling
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    #Flatten Of Nodes
    tf.keras.layers.Flatten(),
    #128 Nodes input
    tf.keras.layers.Dense(128, activation="relu"),
    #NUM_CATEGORIES distribution
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")])
    
    #Comipiling Technique
    model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
    )
    return model

if __name__ == "__main__":
    main()
