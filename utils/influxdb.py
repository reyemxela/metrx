from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from logging import getLogger

class DB:
  def __init__(self, host, token, org, bucket):
    self.logger = getLogger(__name__)

    self.host = host
    self.token = token
    self.org = org
    self.bucket = bucket
    
    self.fails = {}

    self.client = InfluxDBClient(
      url=self.host,
      token=self.token,
      org=self.org,
    )
    self.api = self.client.write_api(write_options=SYNCHRONOUS)

  def write(self, name, data):
    """`data` should be a dict in the form:

    ```
    {
      'measurement': 'name',
      'tags': {'tag1': 1},
      'fields': {'field1': 1},
      'time': 1
    }
    ```
    `measurement` and `fields` are the only required keys
    """
    self.fails.setdefault(name, 0)

    try:
      self.api.write(bucket=self.bucket, record=Point.from_dict(data))
    except Exception as e:
      if self.fails[name] < 5:
        if type(e) is ApiException:
          self.logger.error(e.message)
        else:
          self.logger.error(e)

        self.fails[name] += 1
        if self.fails[name] >= 5:
          self.logger.error(f'{name} has failed 5 times in a row, disabling log output')
    else:
      self.fails[name] = 0
