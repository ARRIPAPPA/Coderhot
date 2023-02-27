from os import getenv
from pymongo import MongoClient
from logging import StreamHandler, getLogger, basicConfig, ERROR, INFO
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from os.path import exists
from os import system, getcwd
from sys import exit
from subprocess import run as subprocess_run
from shutil import rmtree


###############------init aria------###############
subprocess_run(["chmod", "+x", "aria.sh"])
subprocess_run("./aria.sh", shell=True)

###############------Logging------###############
if exists("Logging.txt"):
    with open("Logging.txt", "r+") as f_d:
        f_d.truncate(0)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "Logging.txt", maxBytes=50000000, backupCount=10, encoding="utf-8"
        ),
        StreamHandler(),
    ],
)

getLogger("telethon").setLevel(ERROR)
getLogger("pyrogram").setLevel(ERROR)
LOGGER = getLogger()


###############------Download_Config------###############
CONFIG_FILE_URL = getenv("CONFIG_FILE_URL", False)
if CONFIG_FILE_URL and str(CONFIG_FILE_URL).startswith("http"):
    LOGGER.info(f"🔶Downloading Config File From URL {CONFIG_FILE_URL}")
    system(f"wget -O config.env {str(CONFIG_FILE_URL)}")


###############------Import_Config------###############
if exists('config.env'):
    LOGGER.info(f"🔶Importing Config File")
    load_dotenv('config.env')


###############------Import_Bot_Config------###############
if exists('botconfig.env'):
    LOGGER.info(f"🔶Importing Bot Config File")
    load_dotenv('botconfig.env')


###############------Get_Data_From_MongoDB------###############
def get_mongo_data(MONGODB_URI, BOT_USERNAME, id, colz):
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[BOT_USERNAME]
        col = mongo_db[colz]
        LOGGER.info(f"🔶Getting Data From Database From MongoDB With Database Name {BOT_USERNAME} And ID  {id}")
        item_details = col.find({"id" : id})
        data = False
        for item in item_details:
                data = item.get('data')
        if data:
            LOGGER.info("🟢Data Found In Database")
            return data
        else:
            LOGGER.info("🟡Data Not Found In Database")
            return "{}"


###############------Config_Section------###############
class Config:
    try:
        API_ID = int(getenv("API_ID",""))
    except:
        LOGGER.info("🔶Invalid Config")
        exit()
    API_HASH = getenv("API_HASH","")
    TOKEN = getenv("TOKEN","")
    USE_PYROGRAM = True
    USE_SESSION_STRING = getenv("USE_SESSION_STRING", False)
    SESSION_STRING = getenv("SESSION_STRING","")
    RUNNING_TASK_LIMIT = int(getenv("RUNNING_TASK_LIMIT",""))
    FINISHED_PROGRESS_STR = getenv("FINISHED_PROGRESS_STR", '■')
    UNFINISHED_PROGRESS_STR = getenv("UNFINISHED_PROGRESS_STR", '□')
    try:
        AUTH_GROUP_ID = int(getenv("AUTH_GROUP_ID",""))
    except:
        LOGGER.info("🔶Auth Group ID Not Found, Pyrogram Download and Upload Will Not Work In Group")
        AUTH_GROUP_ID = False
    NAME = "Nik66Bots"
    DOWNLOAD_DIR = f"{getcwd()}/downloads"
    OWNER_ID = int(getenv("OWNER_ID",""))
    SUDO_USERS = [int(x) for x in getenv("SUDO_USERS","").split(" ")]
    ALLOWED_CHATS = SUDO_USERS.copy()
    SAVE_TO_DATABASE = eval(getenv("SAVE_TO_DATABASE",""))
    if SAVE_TO_DATABASE:
        MONGODB_URI = getenv("MONGODB_URI","")
        COLLECTION_NAME = "USER_DATA"
        SAVE_ID = "Nik66"
        DATA = eval(get_mongo_data(MONGODB_URI, NAME, SAVE_ID, COLLECTION_NAME))
    else:
        LOGGER.info("🔶Not Using MongoDB Database")
        DATA = {}
    LOGGER = LOGGER
    try:
        RESTART_NOTIFY_ID = int(getenv("RESTART_NOTIFY_ID",""))
        LOGGER.info("🔶Restart Notification ID Found")
    except:
        RESTART_NOTIFY_ID = False
        LOGGER.info("🔶Restart Notification ID Not Found")


if exists(Config.DOWNLOAD_DIR):
    LOGGER.info("🔶Clearing Download Directory.")
    rmtree(Config.DOWNLOAD_DIR)