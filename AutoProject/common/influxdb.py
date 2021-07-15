from datetime import datetime

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxdbClient:
    def __init__(self, url="http://192.168.1.120:8086", org="admin", bucket="auto_test"):
        # You can generate a Token from the "Tokens Tab" in the UI
        token = "DDPD7qqzXMZAHxXJI-ZIoiKQaiQfDmVI1Eiq_IMvoiBSZnCHTKo4Wceh3dd0gGnjzn_SVAwHTgAci8QyvXIjTw=="
        self.org = org
        self.bucket = bucket

        self.client = InfluxDBClient(url=url, token=token)

    def InfluxdbWrite(self, data):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(self.bucket, self.org, data)

    def InfluxdbRead(self, data):
        query = f'from(bucket: \\"{self.bucket}\\") |> range(start: -1h)'
        tables = self.client.query_api().query(query, org=self.org)

    def close(self):
        self.client.close()