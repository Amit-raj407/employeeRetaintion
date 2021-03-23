import json
import _pickle as cPickle
import numpy as np

with open('model.pkl', 'rb') as f:
    rf = cPickle.load(f)

with open("info.json") as file:
    json_object = json.loads(file.read())

cols = ['satisfaction_level', 'Work_accident', 'promotion_last_5years', 'department_accounting', 'department_hr', 'department_marketing', 'department_sales', 'department_support', 'salary_low', 'salary_medium']
d = {i:0 for i in cols}
for i in json_object:
    if i in d:
        d[i] = float(json_object[i])
    else:
        x = str(i)+'_'+str(json_object[i])
        if x in d:
            d[x] = 1
            
val = rf.predict(np.array(list(d.values())).reshape(1, 10))[0]
