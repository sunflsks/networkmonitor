# Code to upload data to the server

import requests
import constants
from pydantic import BaseModel
from typing import List
from cellular import PingResult
from utils import LockableObject


class PingResultList(BaseModel):
    __root__: List[PingResult]


def upload_data(results: List[PingResult]):
    print("Uploading data to the server...")

    if results == []:
        print("No data to upload.")
        return
    ping_list = PingResultList.parse_obj(results).dict()
    upload_dict = {"points": ping_list["__root__"], "device": constants.DEVICE}

    r = requests.post(f"{constants.SERVER_URL}/upload", json=upload_dict)
    print(f"Uploaded Ping Result: Response is '{r}'\n")
