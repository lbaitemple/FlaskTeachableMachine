import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import glob, os

def classify(folder, aiclass):


    if (aiclass['model'] == None):
        list_of_files = glob.glob(os.path.join(folder, "*.h5"))  # * means all if need specific format then *.csv
        mfile = max(list_of_files, key=os.path.getctime)
    else:
        mfile=os.path.join(folder, aiclass['model'])

    if (aiclass['class'] == None):
        list_of_files = glob.glob(os.path.join(folder, "*.txt"))  # * means all if need specific format then *.csv
        lfile = max(list_of_files, key=os.path.getctime)
    else:
        lfile=os.path.join(folder, aiclass['class'])

    if (aiclass['picture'] != None):
        ifile=os.path.join(folder, aiclass['picture'])
    else:
        return None

    labels_path = lfile
    # open input file label.txt
    labelsfile = open(labels_path, 'r')

    # initialize classes and read in lines until there are no more
    classes = []
    line = labelsfile.readline()
    while line:
        # retrieve just class name and append to classes
        classes.append(line.split(' ', 1)[1].rstrip())
        line = labelsfile.readline()
    # close label file
    labelsfile.close()


    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model(mfile)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(ifile)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)


    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    return classes[np.argmax(prediction)]
