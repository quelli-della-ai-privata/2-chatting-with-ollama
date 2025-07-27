import os, requests

MODEL = "llama3.1:8b"

def chat(args):
  inp = args.get("input", "")
  out = f"Welcome to {MODEL}."
  if inp != "":
      base = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
      url = f"{base}/api/generate"
      msg = {"model": MODEL, "prompt": inp, "stream": False}
      res = requests.post(url, json=msg, stream=False).json()
      out = res.get("response", "No response from model.")

  return { "output": out}
