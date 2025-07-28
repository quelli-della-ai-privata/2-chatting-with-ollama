import os, subprocess, logging
import pytest
from dotenv import load_dotenv

@pytest.fixture(scope='session', autouse=True)
def configure_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="session", autouse=True)
def set_env():

    if not os.path.exists(os.path.expanduser("~/.wskprops")):
        raise pytest.UsageError("You need to login to execute integration tests")

    # load secrets
    command = ["ops", "-config", "-dump"]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout

    # Parse the output and set environment variables
    for line in output.splitlines():
        try:
            key, value = line.split('=', 1)
            os.environ[key] = value
            print("OK:", key)
        except:
            print("ERR:", line)

    # override with testenv
    load_dotenv(".env")
    load_dotenv("tests/.env", override=True)