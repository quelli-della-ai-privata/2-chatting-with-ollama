#--kind python:default
#--web true
import hello
def main(args):
  return { "body": hello.hello(args) }
