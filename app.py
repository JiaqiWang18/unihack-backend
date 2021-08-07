from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr.ocr import ImageToText
#from bixin import predict
from aws_sentiment.Utils import preprocessText, AWSWriteTxt
from aws_sentiment.main import makePrediction
from aws_sentiment.Identifier import isRenZha

app = Flask(__name__)
CORS(app)


@app.route('/api/getText', methods=["POST"])
def upload_image():
    try:
        # check if the post request has the file part
        file = request.files['file']
        text = ImageToText(file)
        return jsonify({"text":text})
    except Exception as err:
        return "Error, image not received."

@app.route('/api/predict', methods=["POST"])
def upload_image():
    try:
        # check if the post request has the file part
        textList = request.text
        textList = preprocessText(textList)
        AWSWriteTxt(textList,"input.txt")
        DICT,TARGET_SENTI = makePrediction("input.txt")
        score, report = isRenZha(TARGET_SENTI)

        return jsonify({"text":text,
                        "DICT":DICT,
                        "TARGET_SENTI":TARGET_SENTI,
                        "score":score,
                        "report":report})
    except Exception as err:
        return "Error, text not detected."


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
