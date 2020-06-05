from flask import Flask, render_template, request
import pickle
import json
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

#make the database dictionary accessable to all pages
dic = []
@app.route("/detect_fraud", methods=['POST', 'GET'])
def detect_fraud():
    with open('../data/locker.json', 'r+') as file:
        data = json.load(file)
        for i in range(len(data)):
            dic.append(data[str(i)])
    return render_template('detect_fraud.html', data=dic)

@app.route("/details", methods=['POST','GET'])
def details():
    id = int(request.args.get('id'))
    entry = None
    for row in dic:
        print(type(row['object_id']), type(id))
        if row['object_id'] == id:
            entry = row
            print("found a match for details page")
            break
        print("did not match the id")
    return render_template('details.html', id=id, data=entry)

if __name__=='__main__':
    app.run(debug=True)

# External functions go here
