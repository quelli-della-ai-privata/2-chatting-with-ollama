import os, requests as req, json
import socket, traceback, time

def url(args, cmd):
  apihost = args.get("OLLAMA_API_HOST", os.getenv("OLLAMA_API_HOST", ""))
  return f"{apihost}/api/{cmd}"

def stream(args, lines, state=None):
  out = ""
  sock = None
  addr = (args.get("STREAM_HOST", ""),int(args.get("STREAM_PORT") or "0"))
  if addr[0] and addr:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.connect(addr)
    print(addr, sock)
    if state:
      buf = json.dumps(state).encode("utf-8")
      #print(buf)
      sock.sendall(buf)
      time.sleep(0.01)  # give some time to process the state

  for line in lines:
    msg = {}
    # parse lines, cah be
    # a string
    # { "response" : ...} 
    # { "state": .. }
    try:
      jo = json.loads(line.decode("utf-8"))
      if "state" in jo:
        msg["state"] =  jo.get("state", "")
      if "response" in jo:
        res =jo.get("response", "")
        msg["output"] = res
        out += res
    except:
      msg["output"] = line 
      out += line
    
    if sock is not None:
        buf = json.dumps(msg).encode("utf-8") 
        print(buf)
        sock.sendall(buf)
  if sock is not None:
    sock.close()
  return out

def ask(args, model, inp):
    msg = { "model": model, "prompt": inp, "stream": True }
    return req.post(url(args, "generate"), json=msg, stream=True).iter_lines()

def models(args, search=None):
    msg = {}
    api = url(args, "tags")
    data = req.get(api).json()
    msg["response"] = "models available:\n"
    yield json.dumps(msg).encode("utf-8")
    for model in data.get("models", []):
      time.sleep(0.1)
      name = model.get("name", "")
      if search and name.startswith(search):
        msg["response"] = f"selected {name}\n"
        msg["state"] = name
        yield json.dumps(msg).encode("utf-8")
        break
      msg["response"] = name+"\n"
      yield json.dumps(msg).encode("utf-8")

USAGE= """Welcome to Ollama.
Type `@` to see available models.
Type `@prefix` to select a model."
"""

NOAPIHOST="""No OLLAMA_API_HOST set.
Please use `ops env add OLLAMA_API_HOST=<url>`
to set it and redeploy.
"""

def chat(args):
  if args.get("OLLAMA_API_HOST", os.getenv("OLLAMA_API_HOST", "")) == "":
    return {"output": NOAPIHOST}

  model = args.get("state", "")
  title = args.get("title", "")
  state = {"state": model }
  inp = args.get("input", "")
  out = USAGE
  print(f"model={model} title={title}")
  if inp == "@":
    lines = models(args)
    out = stream(args, lines, state)
  elif inp.startswith("@"):
    lines = models(args, inp[1:])
    out = stream(args, lines, state)
  elif inp != "":
    if model != "": 
      lines = ask(args, model, inp)
    else:
      lines =["No model selected.\n", "Please use @prefix to select a model."]
    out = stream(args, lines, state)
  
  return { "output": out, "streaming": True }
