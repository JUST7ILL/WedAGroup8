import argparse
import logging
import os
import sys
import time

import numpy as np
import pandas

from BTinterface import BTInterface
from maze import Action, Maze
from score import Scoreboard, ScoreboardFake

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# TODO : Fill in the following information
TEAM_NAME = "Wed_AFTN_8"
SERVER_URL = "http://140.112.175.18:5000/"
MAZE_FILE = "data/small_maze.csv"
BT_PORT = "COM4"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument(
        "--team-name", default=TEAM_NAME, help="Your team name", type=str
    )
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    return parser.parse_args()

    
def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str):
    maze = Maze(maze_file)
    point = Scoreboard(team_name, server_url)
    # point = ScoreboardFake("your team name", "data/fakeUID.csv") # for local testing
    interface = BTInterface(port=bt_port)
    # TODO : Initialize necessary variables
    if mode == "0":
        log.info("Mode 0: For treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible

    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.
        # t_str = maze.actions_to_str(maze.getActions(maze.strategy_2(maze.node_dict[1],maze.node_dict[12])))
        lastuid = 0
        t_str = "ff"
        for c in t_str:
            interface.send_action(c)
            while True:
                if interface.bt.waiting():
                    rt = interface.get_byte()
                    if rt == "0x6e": break
                    nowuid = rt[2:]
                    if lastuid == nowuid: continue
                    # print(nowuid)
                    point.add_UID(nowuid)
                    lastuid = nowuid
                    break
        while True:
            a = 1
    else:
        log.error("Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
