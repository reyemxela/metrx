import requests
from logging import getLogger

class Module:
  def __init__(self, name, config, db):
    self.logger = getLogger(__name__)
    self.name = name
    self.db = db

    self.host = config.get('host')
    self.token = config.get('token')

    self.session = requests.Session()
    self.session.headers = {'Accept': 'application/json', 'X-Plex-Token': self.token}

  def run(self):
    resp = self.session.get(f'{self.host}/status/sessions')
    if not resp:
      self.logger.error(f'{self.name} - {resp.content.decode()}')
      return
    resp = resp.json()
    sessions = resp['MediaContainer']['size']
    transcodes = 0
    if sessions > 0:
      for meta in resp['MediaContainer']['Metadata']:
        if 'TranscodeSession' in meta:
          if meta['TranscodeSession']['videoDecision'] == 'transcode':
            transcodes += 1

    data = {
      'measurement': self.name,
      'fields': {
        'sessions': sessions,
        'transcodes': transcodes
      }
    }
    self.logger.debug(data)
    self.db.write(self.name, data)
