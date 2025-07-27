import os, requests

def models(args):
  
  base = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
  url = f"{base}/api/tags"

  # listo i mdels
  models = requests.get(url).json()
  names = [ i.get("name") for i in models.get("models")]
  out =  "\n".join(names)

  return {
    "output": out
  }
  