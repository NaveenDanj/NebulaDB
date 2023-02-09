import requests
import os
from lib.core.Instance import Instance


class Connection:

    def __init__(self, credential_dict):
        self.credential_dict = credential_dict
        self.CONNECTION_ESTABLISHED = False
        self.Instance = None

    def connect(self):
        url = os.getenv("BASE_URL") + "/api/connection"
        payload = {
            "connection_id": self.credential_dict["connection_id"],
            "instance_name": self.credential_dict["instance_name"],
            "secret": self.credential_dict["secret"]
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("Connection extablished successfully!")
            self.Instance = Instance({
                "connection_id":
                self.credential_dict["connection_id"],
                "instance_name":
                self.credential_dict["instance_name"],
                "secret":
                self.credential_dict["secret"]
            })
            self.CONNECTION_ESTABLISHED = True
        else:
            self.CONNECTION_ESTABLISHED = False
            raise Exception("Connection failed!")

    def get_connection_status(self):
        return self.CONNECTION_ESTABLISHED

    def get_instance(self):
        return self.Instance