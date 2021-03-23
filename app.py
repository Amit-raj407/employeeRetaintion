from flask import Flask, render_template, request
import numpy as np
import _pickle as cPickle
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


def func():
    with open('model.pkl', 'rb') as f:
        rf = cPickle.load(f)
    with open("info.json") as file:
        json_object = json.loads(file.read())

    cols = ['satisfaction_level', 'Work_accident', 'promotion_last_5years', 'department_accounting', 'department_hr',
            'department_marketing', 'department_sales', 'department_support', 'salary_low', 'salary_medium']
    d = {i: 0 for i in cols}
    for i in json_object:
        if i in d:
            d[i] = float(json_object[i])
        else:
            x = str(i)+'_'+str(json_object[i])
            if x in d:
                d[x] = 1

    val = rf.predict(np.array(list(d.values())).reshape(1, 10))[0]
    return val

@app.route("/predict", methods=["POST"])
def predict():
    data = request.form.to_dict()
    # return data
    data["satisfaction_level"] = int(data["satisfaction_level"])/100
    data["last_evaluation"] = int(data["last_evaluation"])/100
    if(int(data["salary"]) < 15000):
        data["salary"] = "low"
    elif(15000 < int(data["salary"]) < 50000):
        data["salary"] = "medium"
    else:
        data["salary"] = "high"
    json_object = json.dumps(data)
    with open("info.json", "w") as f:
        f.write(json_object)
    val = func()
    if(val == 0):
        str = "not Leave"
    else:
        str = "Leave"
    return render_template("result.html",name=data["Name"],result=str)
    # return "Data Saved"


if __name__ == "__main__":
    app.run(debug=True)
