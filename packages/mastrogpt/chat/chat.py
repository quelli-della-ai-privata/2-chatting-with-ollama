import os, requests as req, json, socket


def url(args):
  apihost = args.get("MY_OLLAMA_API_HOST", args.get("OLLAMA_API_HOST", os.getenv("OLLAMA_API_HOST")))
  return f"{apihost}/api/generate"

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
  llm = url(args)
  model = args.get("OLLAMA_MODEL", "no model selected")
  out = f"Welcome to {model}"
  inp = args.get("input", "")
  if inp != "":
    msg = { "model": model, "prompt": inp, "stream": True }
    lines = req.post(llm, json=msg, stream=True).iter_lines()
    out = stream(args, lines)
  return { "output": out, "streaming": True}
