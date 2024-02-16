import requests
from logging import getLogger

class Module:
  def __init__(self, name, config, db):
    self.logger = getLogger(__name__)
    self.name = name
    self.db = db

    self.host = config.get('host')
    self.apikey = config.get('apikey')

    self.session = requests.Session()

  def run(self):
    resp = self.session.get(f'{self.host}/sabnzbd/api', params={'output': 'json', 'apikey': self.apikey, 'mode': 'queue', 'limit': -1})
    if not resp:
      self.logger.error(f'{self.name} - {resp.content.decode()}')
      return
    queue = resp.json()['queue']
    downloads = queue['noofslots_total']
    mbleft = queue['mbleft']
    kbpersec = queue['kbpersec']
    speedlimit = int(queue['speedlimit_abs']) / 1024 # report speedlimit in kbps, to match speed

    data = {
      'measurement': self.name,
      'fields': {
        'downloads': int(downloads),
        'mbleft': float(mbleft),
        'kbpersec': float(kbpersec),
        'speedlimit': int(speedlimit),
      }
    }
    self.logger.debug(data)
    self.db.write(self.name, data)
