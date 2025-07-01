import os, requests as req, json, socket

MODEL="llama3.1:8b"

def url(args):
  host = args.get("OLLAMA_API_HOST", os.getenv("OLLAMA_API_HOST"))
  return f"{host}/api/generate"

import json, socket, traceback
def stream(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT"))
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        dec = json.loads(line.decode("utf-8")).get("response")
        msg = {"output": dec }
        out += dec
        s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out

def chat(args):
  out = f"Welcome to {MODEL}"
  inp = args.get("input", "")
  if inp != "":
    if inp == "llama":
      MODEL="llama3.1:8b"
      inp = "Who are you?"
    elif inp == "deepseek":
      MODEL="deepseek-r1:32b"
      inp = "Who are you?"
    elif inp == "mistral":
      MODEL="mistral:latest"
      inp = "Who are you?"
    msg = { "model": MODEL, "prompt": inp, "stream": True }
    lines = req.post(url(args), json=msg, stream=True).iter_lines()
    out = stream(args, lines)
  return { "output": out, "streaming": True}
