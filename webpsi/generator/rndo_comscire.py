from webpsi.generator.base import Generator
import requests
import os

class Randonautica_QRNG(Generator, id='rndo', bit_numbering=Generator.BitNumbering.UNKNOWN):
    def get_bytes(self, length):
        session = requests.Session()
        try:
            response = session.get(f'https://api.qrng.rndo.it/api/json/randhex?device_id=QWR70154&length={length}', verify=False)
            response.raise_for_status()
            return bytes.fromhex(response.json())
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
