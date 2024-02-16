import requests
from logging import getLogger

class Module:
  def __init__(self, name, config, db):
    self.logger = getLogger(__name__)
    self.name = name
    self.db = db

    self.host = config.get('host')
    self.username = config.get('username')
    self.password = config.get('password')

    self.session = requests.Session()
    self.loggedin = False

  def run(self):
    if not self.loggedin:
      resp = self.session.post(f'{self.host}/api/v2/auth/login', params={'username': self.username, 'password': self.password})
      if not resp:
        return
      self.loggedin = True

    resp = self.session.get(f'{self.host}/api/v2/transfer/info')
    if not resp:
      self.logger.error(f'{self.name} - {resp.content.decode()}')
      return
    resp = resp.json()
    dl_speed = resp.get('dl_info_speed')
    dl_limit = resp.get('dl_rate_limit')
    up_speed = resp.get('up_info_speed')
    up_limit = resp.get('up_rate_limit')

    resp = self.session.get(f'{self.host}/api/v2/torrents/count')
    if resp:
      torrent_count = int(resp.content.decode())
    else:
      # torrents/count is a recent API addition, so don't error out if it fails
      torrent_count = None

    data = {
      'measurement': self.name,
      'fields': {
        'dl_speed': int(dl_speed),
        'dl_limit': int(dl_limit),
        'up_speed': int(up_speed),
        'up_limit': int(up_limit),
        'torrent_count': torrent_count,
      },
    }
    self.logger.debug(data)
    self.db.write(self.name, data)
