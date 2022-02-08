#!/usr/bin/python3
import logger
from logger import log
import yaml
import sys
from token_distribute import Distribute
from settings import load_user_param, user_param

def run(config_file: str):
    with open(config_file, "r", encoding="utf8") as file:
        user: dict = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    load_user_param(user)
    logger.init_loger(user_param.wax_account)
    distribute = Distribute()
    distribute.start()

def main():
    try:
        user_yml = "user.yml"
        if len(sys.argv) == 2:
            user_yml = sys.argv[1]
        run(user_yml)
    except Exception:
        log.exception("distribute error")

if __name__ == '__main__':
    main()
