import logging
import os
from datetime import datetime
from pathlib import Path

logger_filepath = Path(os.getcwd() + f'/app/logs/{datetime.now().strftime("%m-%d-%Y")}.log')
if not os.path.isdir(Path(os.getcwd()) / "app/logs/"):
    os.mkdir(Path(os.getcwd() + "/app/logs/"))
logging.basicConfig(
    filename=logger_filepath,
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s - %(message)s",
    filemode="w",
)