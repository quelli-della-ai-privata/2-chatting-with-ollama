#--kind python:default
#--web true
# TODO: models - add the key

import models
def main(args):
  return { "body": models.models(args) }
