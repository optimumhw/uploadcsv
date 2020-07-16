import json
import requests
import datetime
import csv
import os
import sys

class APIHelper():

    def __init__(self, domain, user, password ):

        self.USER = user
        self.PASSWORD = password
        self.API_DOMAIN = domain

    def getSessionToken(self):
        url = 'https://' + self.API_DOMAIN + '/v1/oauth/token'

        headers = {}
        headers['content-type'] = 'application/json'

        payload = {}
        payload['email'] = self.USER
        payload['password'] = self.PASSWORD
        payload['grant_type'] = 'password'

        r = requests.post(url, data=str(payload).replace("'", '"'), headers=headers)
        dict = json.loads(r.text)

        return (r.status_code, dict['accessToken'])

    def getServiceHeaders(self, token):
        bearer_token = 'bearer ' + token  # note the space

        headers = {}
        headers['content-type'] = 'application/json'
        headers['Authorization'] = bearer_token
        return headers

    def get_csv_data(self, filePath ):

        with open(filePath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            firstRow = True
            payloads = []
            for row in reader:
                if firstRow :
                    firstRow = False
                    point_id = row[1]
                    continue

                ts = row[0]
                dt = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M')
                thisSliceTime = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

                hash = {}
                hash['id'] = point_id
                hash['value'] = row[1]
                hash['timestamp'] = thisSliceTime

                payloads.append(hash)

            return payloads


    def upsert(self, payloads):
        url = 'https://' + self.API_DOMAIN + '/v1/data/upsert'

        headers = self.getServiceHeaders()
        r = requests.post(url, data=str(payloads).replace("'", '"'), headers=headers)
        return r.status_code

if __name__ == '__main__':

    tesla_user = os.environ['TESLA_USER']
    tesla_password = os.environ['TESLA_PASSWORD']
    api_domain = sys.argv[1]
    csv_path = sys.argv[2]

    print('user: ',tesla_user)
    print('domain: ',api_domain)
    print('csv: ', csv_path)

    helper = APIHelper(api_domain, tesla_user, tesla_password)

    status, token = helper.getSessionToken()
    if status != 200:
        print('status: %d - Could not get token' % status)
        exit()

    print("token is: ", token)

    headers = helper.getServiceHeaders(token)

    payloads = helper.get_csv_data( csv_path )

    print(payloads)

    status_code = helper.upsert(payloads)

    print('done')
