import os
import logging
logging.basicConfig(filename='logs.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('tg_feed')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

ACCEPTED_CHANNELS = [
    1320343625,  # !internet!
    1224122704,  # afro
    1009232144,  # двач
    1509268340,  # котёночек
    1579433289,  # акб
    1545924621,  # ачё
    1332405564,  # ачё2
    1137657151,  # ретранслятор
    1096963058,  # 4chan
    1143742161,  # мои любимые юморески
    1057408216,  # IT-юмор
    1321922060,  # female memes
    1081170974,  # profunctor
    1641545987,  # кек
]
TARGET_CHANNEL = 1407901668
TRASH_CHANNEL = 1611196915
ACCEPTED_URLS = ['teletype', 'telegra']