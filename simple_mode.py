from config import config as mo_config
import login
import os
import sys
import json
from argparse import ArgumentParser
import logging
import requests,threading

logging.basicConfig(
    filename='login_tool.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s\
             %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


parser = ArgumentParser()
parser.add_argument("-acc", "--account",
                    help="game account", dest="account", default=None)
parser.add_argument("-pwd", "--password",
                    help="game password", dest="password", default=None)

parser.add_argument("-mode",
                    help="start from which exe.Recommand Win7:login Win10:game", dest="mode", default='game')


args = vars(parser.parse_args())

if __name__ == "__main__":
    if os.path.isfile("config.json"):
        config_dict = json.load(open('config.json', 'r'))
    else:
        logging.error('Not found config.json')
        sys.exit(0)
    # args weight is more than config.json , so load args last.
    for k, v in args.items():
        if v is not None:
            config_dict[k] = v
    config = mo_config(**config_dict)
    session = login.get_session()
    threading.Thread(target=login.get_captcha,args=(session,)).start()
    if args['account'] is not None and args['password'] is not None:
        account = args['account']
        password = args['password']
    else:
        account = input('Account : ')
        password = input('Password : ')

    try:
        moop = login.login(session=session,
                           account=account,
                           password=password,
                           captcha_code=input("input captcha code: "))
        if args['mode'] == 'game':
            login.open_game(moop, config.game_path)
        elif args['mode'] == 'login':
            login.open_login(moop, config.login_path)
    except login.LoginError as e:
        logging.warning(e.message)
    except BaseException as e:
        logging.warning(e)
