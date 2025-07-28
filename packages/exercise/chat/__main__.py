#--kind python:default
#--web true
import chat
def main(args):
  return { "body": chat.chat(args) }
