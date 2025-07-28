MODEL = "llama3.1:8b"

def chat(args):
  # TODO: default message
  out = "chat"

  inp = args.get("input", "")
  if inp != "":
      
      # TODO: chat - get the url
      url = "???"
      
      # TODO: chat - prepare the message 
      msg = {}
      
      # TODO: chat - send the message ollama
      res = {}

      # TODO: chat: return the response
      out =  "???"

  return { "output": out}
