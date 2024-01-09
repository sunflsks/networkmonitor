# Code to upload data to the server

import requests
from pydantic import BaseModel
from typing import List
from cellular import PingResult
from utils import LockableObject

DEVICE = "test"
SERVER_URL = "http://mr-radar.local:3000"

class PingResultList(BaseModel):
    __root__: List[PingResult]

def upload_data(results: LockableObject):
    print("Uploading data to the server...")

    with results:
        if results.value == []:
            print("No data to upload.")
            return
        ping_list = PingResultList.parse_obj(results.value).dict()
        upload_dict = {"points": ping_list["__root__"], "device": DEVICE}

        r = requests.post(f"{SERVER_URL}/upload", json=upload_dict)
        print(r)
        results.value = []
