from datetime import datetime
from flask import Flask, request, abort, jsonify
import paho.mqtt.client as mqtt
import logging, os, json
from pred import classify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


###
##  curl -u lbai:test -F "picture=@pic2.jpg" -F "model=@keras_model.h5" -F "class=@labels.txt" -F "format=json" http://127.0.0.1:5000/upload
##  curl -u lbai:test -F "picture=@pic2.jpg" -F "model=@keras_model.h5" -F "class=@labels.txt" -F "format=text" http://127.0.0.1:5000/upload
###

app = Flask(__name__)
auth = HTTPBasicAuth()
#users = {
#    "lbai": generate_password_hash("test"),
#    "mike": generate_password_hash("test")
#}
# load password file. To create a user use python3 createuser.py -u username -p password

with open('passwd.txt') as json_file:
    users = json.load(json_file)
#with open('passwd.txt', 'w') as outfile:
#    json.dump(users, outfile)

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route("/classfy", methods=["POST"])
@auth.login_required
def classfy():
    # data format
    data = request.form.to_dict(flat=True)

    # check autheneication
    folder=auth.current_user()
    # check is the current_user has a folder, if the server does not
    # have the folder, create one
    if not os.path.exists(folder):
        os.makedirs(folder)
    #bauth = self.headers['Authorization'].split(' ')[1]
    #load files to be classfied
    content = ['class', 'model', 'picture']
    aiclass={}

    for fi in content:
        try:
            # upload file into user's folder and set the name in dict aiclass
            file = request.files[fi]
            aiclass[fi]=file.filename
            file.save(os.path.join(folder, file.filename))
        except:
            # if no option is given, set  the file name as None
            aiclass[fi] = None

    pred=classify(folder, aiclass)
    #print(data['output'])
    if pred == None:
        if (data.get('format')=='json'):
            return jsonify({'status': 'failed', 'reason': 'need picture file'}), 300
        else:
            return 'need picture file', 300
    else:
        if (data.get('format')=='json'):
            return jsonify({'status': 'success', 'pred': pred}), 200
        else:
            return pred+'\n', 200
    return ""


@app.route('/webhook', methods=['POST'])
def webhook():
        # get client from cloudmqtt
        client = mqtt.Client()
        client.username_pw_set("pspniyjc", "sBm4EpaDgRe5")
        client.connect("m16.cloudmqtt.com", 12247, 60)
        if request.method == 'POST':
                data=request.json
                #publush the topic with the data
                client.publish(data['topic'], data['value'])
                debugstr=str(datetime.now()) +": "+ data['topic'] + " - " + data['value']
                logging.debug(debugstr)
                return jsonify({'status':'success', 'time':datetime.now()}), 200
        else:
                abort(400)

if __name__ == '__main__':
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        logging.basicConfig(filename='tmp.log',
                            format='%(levelname)s %(asctime)s :: %(message)s',
                            level=logging.DEBUG)
        app.run(host='0.0.0.0', port=8080)