from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    QualityMode_Manual=0
    if request.method == 'POST':
        QuantityKG = int(request.form['QuantityKG'])
        NoofCans=float(request.form['NoofCans'])
        Rate=int(request.form['Rate'])
        Rate2=np.log(Rate)
        vendorcode=int(request.form['vendorcode'])
        QualityMode_Manual=request.form['QualityMode_Manual']
        if(QualityMode_Manual=='auto'):
                QualityMode_Manual=1
        else:
            QualityMode_Manual=0

        prediction=model.predict([[QuantityKG,NoofCans,Rate,vendorcode,QualityMode_Manual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry ")
        else:
            return render_template('index.html',prediction_text="You Can See price at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

