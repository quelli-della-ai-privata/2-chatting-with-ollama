import os, json
import bcrypt, secrets, redis
from pathlib import Path
import traceback

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify if hashed password matches password.

    Args:
        password (str): The plain password to verify
        hashed_password (str): The saved hashed password

    Returns:
        bool: True if hashed password matches password. False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_and_save_token(args) -> str:
    """
    Generate a token for the user and save it in redis.
    """
    username = args.get("username")
    rd = redis.from_url(args.get("REDIS_URL", os.getenv("REDIS_URL")))
    prefix = args.get("REDIS_PREFIX", os.getenv("REDIS_PREFIX"))
 
    key = secrets.token_urlsafe(32)
    rd.setex(f"{prefix}TOKEN:{username}", 86400, key)
    
    return f"{username}:{key}"

def login(args):
    """
    >>> import login
    >>> args = {}
    >>> login.login(args)
    {'authenticated': False}
    >>> args= {"username":"boh"}
    >>> login.login(args)
    {'authenticated': False}
    >>> args= {"username":"pinocchio", "password": "bad"}
    >>> login.login(args)
    {'authenticated': False}
    >>> args= {"username":"pinocchio", "password": "geppetto", "S3_SECRET_KEY": "123"}
    >>> login.login(args)
    {'authenticated': True, 's3_key': '123'}
    """
        
    res = { "authenticated": False}
    try:
        username = args.get("username")
        password = args.get("password")

        users = json.loads(Path("users.json").read_text())
        #print(users)
        if username != "" and password != "":
            if username in users:
                if verify_password(password, users[username]):
                    token = generate_and_save_token(args)                         
                    res = {
                        "authenticated": True,
                        "token": token,
                        "s3_key": args.get("S3_SECRET_KEY", "")
                    }
                    
    except Exception as e:
        print(str(e))
        traceback.print_exc()
    
    return res

  