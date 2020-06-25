import json
import argparse
from werkzeug.security import generate_password_hash
###
##  To create a user use python3 createuser.py -u username -p password
###

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('--verbose',
    action='store_true',
    help='verbose flag' )
parser.add_argument('-u', action='append')
parser.add_argument('-p', action='append')
args = parser.parse_args()


with open('passwd.txt') as json_file:
    users = json.load(json_file)
try:
    if (users[args.u[0]]):
        print("user exist")
    else:
        users[args.u[0]]=generate_password_hash(args.p[0])
        with open('passwd.txt', 'w') as outfile:
            json.dump(users, outfile)
        print("user added")
except:
    print("user exist")

