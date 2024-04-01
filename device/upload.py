# Code to upload data to the server

import requests
import constants
from pydantic import BaseModel
from typing import List
from cellular import PingResult
from utils import LockableObject, blink_led


class PingResultList(BaseModel):
    __root__: List[PingResult]


def upload_data(results: List[PingResult]) -> None:
    print("Uploading data to the server...")

    if results == []:
        print("No data to upload.")
        return
    ping_list = PingResultList.parse_obj(results).dict()
    upload_dict = {"points": ping_list["__root__"], "device": constants.DEVICE}

    r = requests.post(f"{constants.SERVER_URL}/upload", json=upload_dict)
    if r:
        print(f"UPLOADED SUCCESSFULLY: Response is '{r}'\n")
        blink_led("ACT", 3, 0.1)
    else:
        print(f"ERROR UPLOADING: Response if '{r}'\n")
