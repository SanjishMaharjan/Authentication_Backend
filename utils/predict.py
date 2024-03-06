import keras
from keras.preprocessing import image
import numpy as np
from PIL import Image
import io
from utils.model import model

model.load_weights("./utils/checkpoint_new2.weights.h5")


async def predict_image(contents):
    images = Image.open(io.BytesIO(contents))

    img = np.array(images.resize((256, 256))).reshape(1, 256, 256, 3)

    result = np.argmax(keras.activations.softmax(model.predict(img, verbose=0)))
    confidence = np.max(keras.activations.softmax(model.predict(img, verbose=0)))
    print(confidence)

    result = np.where(result == 1, "real", "fake")

    return (result.item(), confidence)
