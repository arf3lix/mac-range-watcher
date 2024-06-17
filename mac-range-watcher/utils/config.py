import configparser
from utils.logger import get_logger

config = configparser.ConfigParser()
config.read('config.ini')
trackcsv_path = config['paths']['trackcsv']

mac_start = config['mac_range']['start_mac']
mac_end = config['mac_range']['end_mac']

blue_limit = config['range_config']['blue_alert']
yellow_limit = config['range_config']['yellow_alert']
red_limit = config['range_config']['red_alert']