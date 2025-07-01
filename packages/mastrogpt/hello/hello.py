def hello(args):
  name = args.get("input", "world")
  return { "output": f"Hello, {name}" }
