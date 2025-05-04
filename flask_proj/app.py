import pickle
from cv2 import imread
import cv2
from PIL import Image, ImageOps
from flask import Flask, render_template, request, request, redirect, url_for
import random, os, shutil
from tensorflow.keras.applications import EfficientNetB0
import numpy as np
np.random.seed(202)

model = EfficientNetB0(weights='imagenet',include_top=False,
                       input_shape=(256,256,3))
clf = pickle.load(open('finalized_model.sav', 'rb'))

def feature_extractor(x):
    array = []
    for i in x:
        img = cv2.imread(os.path.join('static', i))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        img_resized = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)
        array.append(img_resized)
    array = np.array(array, dtype=np.float32)
    feature_extractor = model.predict(array)
    array = feature_extractor.reshape(feature_extractor.shape[0],-1)
    return array

def save_to_folder(target, data):
    # Ensure the folder exists
    os.makedirs(os.path.join('collection', target), exist_ok=True)
    # Append or create the file
    for i in data:
        temp_path = os.path.join('static', i)
        shutil.copy(temp_path, os.path.join('collection', target, i))

app = Flask(__name__)

# List of image filenames (in static folder)
files = os.listdir("static")
class_label = ['ant', 'apple', 'axe', 'banana', 'bear', 'bee', 'camel', 'candle', 'cat', 'dog']
target = random.choice(class_label)

IMAGE_FILES = random.sample(files, 9)


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        if "none" in request.form:
            # Shuffle images on refresh
            images = random.sample(files, 9)
            selected = []
        elif "check" in request.form:
            images = request.form.getlist("images")
            selected = request.form.getlist("selected")

            # Extract features and predict
            predicted_output = clf.predict(feature_extractor(images))
            # Count matches with target
            op = (predicted_output == target).sum()
            if op == 0:
                message = "Try again"
            else:
                selected_output = clf.predict(feature_extractor(selected))
                up = (selected_output == target).sum()
                message = "You are HOOMAN!" if op == up and len(selected) == op else "Try again."
                if 'HOOMAN!' in message:
                    save_to_folder(target, selected)
    else:
        images = random.sample(IMAGE_FILES, len(IMAGE_FILES))
        selected = []

    return render_template("index.html", images=images, selected=selected, 
                           message=message, target=target.upper())


if __name__ == "__main__":
    app.run(debug=True)
