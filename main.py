from flask import Flask, request, render_template, jsonify
import os
import cv2
# import matplotlib.pyplot as plt
from keras.models import load_model
# import urllib.request
from werkzeug.utils import secure_filename
import numpy as np
from time import time

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif',
                          'tif', 'tiff', 'ico', 'bmp',
                          'webp', 'ppm', 'pgm', 'pbm'])

model = load_model('Xception_model_20220710_9761.h5')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    prev = time()
    
    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
            # print(type(file))
            image_file = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file_resize = cv2.resize(image_file, (128, 128), interpolation=cv2.INTER_AREA)
            image_file_resize = image_file_resize.astype('float32') / 255
            # plt.imshow(image_file_resize)
            # print(type(image_file_resize))
        else:
            errors[file.filename] = 'File type is not allowed'

        test_pred = model.predict(np.array([image_file_resize]), verbose=1)
        test_pred_p = test_pred * 100
        test_pred_p = test_pred_p.astype('int32')
        test_pred_p_sorted = np.sort(test_pred_p)
        test_pred_p_sorted = test_pred_p_sorted[:, ::-1]
        test_pred_p_arg = np.argsort(test_pred_p)
        test_pred_p_arg = test_pred_p_arg[:, ::-1]
        test_pred = np.argmax(test_pred, axis=1)
        string = "Showing the last uploaded file<br>" * (len(files) > 1)
        # test_label_1 = np.argmax(test_label, axis=1)

        display_labels = ['0 text', '1 scenic', '2 city', '3 admin', '4 star',
                          '5 photo', '6 human', '7 object', '8 building']
        for i, j in zip(test_pred_p_arg[0], test_pred_p_sorted[0]):
            if j:
                string += ((display_labels[i].ljust(10)+(str(j)+'%').rjust(4))+'<br>')\
                            .replace(' ', '&nbsp;')
    if string.endswith('<br>'): string = string[:-4]
    if success and errors:
        errors['message'] = string  # 'File successfully uploaded<br>'+string
        resp = jsonify(errors)
        resp.status_code = 206
        return resp
    if success:
        now = time()
        resp = jsonify({'message': string, 'time':round(now-prev, 3)})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
