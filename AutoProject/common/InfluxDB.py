from datetime import datetime

import requests


class InfluxdbClient:
    def __init__(self, url="http://192.168.1.120:8086", org="admin", bucket="auto_test"):
        # You can generate a Token from the "Tokens Tab" in the UI
        token = "DDPD7qqzXMZAHxXJI-ZIoiKQaiQfDmVI1Eiq_IMvoiBSZnCHTKo4Wceh3dd0gGnjzn_SVAwHTgAci8QyvXIjTw=="
        self.url = url
        self.headers = {
            "Authorization": f"Token {token}"
        }

    def Write(self, data):
        r = requests.post(f"{self.url}/api/v2/write?org=admin&bucket=auto_test&precision=s",
                          headers=self.headers,
                          data=data)

    def Read(self, data):
        self.headers["Accept"] = 'application/csv'
        self.headers["Content-type"] = 'application/json'
        r = requests.post(f"{self.url}//api/v2/query?org=admin&database=auto_test",
                         headers=self.headers,
                         data="q=SELECT * FROM auto_test.duration")
        print(r.text)
