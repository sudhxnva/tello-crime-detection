
import cv2
import numpy as np
from PIL import Image
from keras import models

# Load the saved model
model = models.load_model('model.h5')
video = cv2.VideoCapture('arson-3.avi')

index = 0


def label_prediction(predictions):
    labels_without_normal = ['Abuse', 'Arrest', 'Arson', 'Assault', 'Burglary', 'Explosion', 'Fighting',
                             'RoadAccidents', 'Robbery', 'Shooting', 'Shoplifting', 'Stealing', 'Vandalism']
    if (predictions[7] == 1):
        return "No Crime"
    else:
        predictions_without_normal = np.delete(predictions, 7)
        max_index = np.where(predictions_without_normal ==
                             np.amax(predictions_without_normal))[0][0]
        if (labels_without_normal[max_index] == 0.0):
            return "No Crime"
        else:
            print(predictions)
            return "POSSIBLE CRIME: " + labels_without_normal[max_index] + " (" + str(round(predictions_without_normal[max_index].item() * 100, 3)) + "%)"


def predict(frame):
    index = index + 1
    if (index % 10 != 0):
        return
    else:
        index = 0

    # Convert the captured frame into RGB
    im = Image.fromarray(frame, 'RGB')

    # Resizing into 64x64 because we trained the model with this image size.
    im = im.resize((64, 64))
    img_array = np.array(im)

    # Our keras model used a 4D tensor, (images x height x width x channel)
    # So changing dimension 64x64x3 into 1x64x64x3
    img_array = np.expand_dims(img_array, axis=0)

    # Calling the predict method on model to predict crime on the image
    prediction = model.predict(img_array)[0]

    return label_prediction(prediction)

    # # if prediction is 0, then show the frame in gray color.
    # if prediction[0] == 0:
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # else:
    #     cv2.waitKey(3000)
