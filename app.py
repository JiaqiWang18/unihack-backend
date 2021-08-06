from flask import Flask, request
from flask_cors import CORS
from make_celery import make_celery

app = Flask(__name__)
CORS(app)


@app.post('/api/predict')
def upload_image():
    try:
        # check if the post request has the file part
        file = request.files['file']
        print(file)
        return "Image uploaded"
    except Exception as err:
        return "Error, image not received."


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
