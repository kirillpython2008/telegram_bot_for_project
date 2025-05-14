from os import getenv

from dadata import Dadata
from dotenv import load_dotenv

load_dotenv()

DADATA_TOKEN = getenv("DADATA_TOKEN")
DADATA_SECRET = getenv("DADATA_SECRET")

dadata = Dadata(token=DADATA_TOKEN,
                secret=DADATA_SECRET)

def check_address(address: str):
    result = dadata.clean("address", address)

    if int(result["fias_level"]) in [8, 9]:
        return result, True
    return "Адрес не найден или не корректен", False
