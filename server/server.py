##from flask import Flask, request, jsonify
##app = Flask(__name__)
import os
from flask import Flask, flash, request, redirect, url_for
from flask import jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
from keras.models import model_from_json

UPLOAD_FOLDER = '/Users/Matthias/Documents/DataScience/fullstack/dogs_vs_cats/server/artifacts/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET','POST'])
def upload_file():
    uploaded_files={}
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_files.add(filename)
    
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    <table>
        <tr>
            <th>Filename</th>
            <th>Thumbnail</th>
        </tr>
        {% for uf in uploaded_files %}
            <tr>
                <td>{{ uf }}</td>
                <td>$100</td>
            </tr>
        {% endfor %}
    </table>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)

@app.route('/predict/<imgnum>')
def predict_image(imgnum):
    zbasednum=imgnum-1
    imgs = os.listdir('../artifacts')
    filename = imgs[zbasednum]
    json_file = open('../artifacts/model.json','r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("../artifacts/model_catsdogs_cpu.h5")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])


@app.route('/hello')
def hello():
    return "Hi"

if __name__ == "__main__":
    print("Starting Python Flask Server for Cats Vs. Dogs Prediction...")
    app.run()