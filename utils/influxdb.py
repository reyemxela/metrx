from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class DB:
  def __init__(self, host, token, org, bucket):
    self.host = host
    self.token = token
    self.org = org
    self.bucket = bucket

    self.client = InfluxDBClient(
      url=self.host,
      token=self.token,
      org=self.org,
    )
    self.api = self.client.write_api(write_options=SYNCHRONOUS)

  def write(self, data):
    self.api.write(bucket=self.bucket, record=Point.from_dict(data))
  
  def close(self):
    self.client.close()