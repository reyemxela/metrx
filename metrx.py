import sys
sys.dont_write_bytecode = True

import os
import time
import yaml
import argparse
import logging
import threading
import signal

import schedule

from utils.influxdb import DB
import modules


def threaded(func):
  job = threading.Thread(target=func)
  job.start()


def register(name, data, db, dryrun):
  try:
    stype = data.get('type')
    interval = data.get('interval')
    config = data.get('config')

    modtype = modules.MODULES.get(stype)
    if modtype is None:
      logging.error(f'{name} - no module found for type "{stype}"')
      return
    
    mod = modtype(name, config, db)
    logging.info(f'Registered {name} ({stype})')

    if not dryrun:
      logging.debug(f'Scheduling {name} to run every {interval} seconds')
      schedule.every(interval).seconds.do(threaded, mod.run)
  except Exception as e:
    logging.error(e)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', '-c', help='Path to config.yaml. Defaults to ./config.yaml or /config/config.yaml')
  parser.add_argument('--debug', action='store_true', help='Turns on debug logging')
  parser.add_argument('--dryrun', action='store_true', help='Only attempts loading config and registering services, then exits')
  args = parser.parse_args()

  configfile = args.config
  debug = args.debug
  dryrun = args.dryrun

  # set up logging
  logging.basicConfig(
    format='{asctime} {name:>16.16s}: {levelname:>8s}: {message}', style='{',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=(logging.DEBUG if debug else logging.INFO)
  )

  # load config file
  if not configfile:
    project_dir = os.path.dirname(__file__)
    for configfile in (
      os.path.join(project_dir, 'config.yaml'),
      os.path.join('/config', 'config.yaml'),
    ):
      if os.path.isfile(configfile):
        break
    else:
      sys.exit('Unable to find config.yaml')

  try:
    with open(configfile) as f:
      config = yaml.safe_load(f)
      logging.info(f'Loaded {configfile}')
  except OSError as e:
    sys.exit(f'Error: {e}')
  
  # set up DB connection
  influxdb_config = config.get('influxdb')
  if not influxdb_config:
    sys.exit('Error: InfluxDB config missing')
  db = DB(**influxdb_config)

  # load all modules from main+custom folders
  modules.load_modules()

  # load/register services
  for name, data in config['services'].items():
    register(name, data, db, dryrun)
  
  if not schedule.get_jobs():
    logging.info('No jobs, exiting')
    return

  # run all on start
  schedule.run_all()

  # main loop
  while True:
    schedule.run_pending()
    time.sleep(1)


def signal_handler(_signal, _frame):
  print('\nExiting')
  sys.exit(0)


if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)
  main()