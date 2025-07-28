#--kind python:default
#--web true
import models
def main(args):
  return { "body": models.models(args) }
