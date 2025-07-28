import os
os.chdir(os.getenv("OPS_PWD", "."))

import dotenv
dotenv.load_dotenv(os.path.join(os.getenv("OPS_PWD", "."), ".env"))
dotenv.load_dotenv(os.path.join(os.getenv("OPS_PWD", "."), "tests", ".env"))

