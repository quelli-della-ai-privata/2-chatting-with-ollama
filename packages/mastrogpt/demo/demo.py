import json

USAGE = "Please type one of 'code', 'chess', 'html', 'form', 'message', 'options'"

FORM = [
  {
      "name": "why",
      "label": "Why do you recommend Apache OpenServerless?",
      "type": "textarea",
      "required": "true"
  },
  {
    "name": "job",
    "label": "What is your job role?",
    "type": "text",
    "required": "true"
  },
  {
    "name": "tone",
    "label": "What tone should the post have?",
    "type": "text",
    "required": "true"
  }
]

HTML = """<div class="max-w-md mx-auto p-6 bg-white shadow-md rounded-lg">
  <h1 class="text-2xl font-bold text-gray-800 mb-6">Sample Form</h1>
  <form action="/submit-your-form-endpoint" method="post" class="space-y-4">
    <div class="flex flex-col">
      <label for="username" class="mb-2 text-sm font-medium text-gray-700">Username:</label>
      <input
        type="text"
        id="username"
        name="username"
        required
        class="p-2 border border-gray-300 rounded-md bg-white text-black focus:ring-2 focus:ring-teal-500 focus:outline-none"
      />
    </div>
    <div class="flex flex-col">
      <label for="password" class="mb-2 text-sm font-medium text-gray-700">Password:</label>
      <input
        type="password"
        id="password"
        name="password"
        required
        class="p-2 border border-gray-300 rounded-md bg-white text-black focus:ring-2 focus:ring-teal-500 focus:outline-none"
      />
    </div>
    <div>
      <button
        type="submit"
        class="w-full py-2 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 focus:ring-2 focus:ring-blue-400 focus:outline-none"
      >
        Login
      </button>
    </div>
  </form>
</div>
"""

CODE = """
def sum_to(n):
    sum = 0
    for i in range(1,n+1):
        sum += i
    return sum
"""

CHESS = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"

def demo(args):
    print(args)
        
    language = None
    code = None
    chess = None
    message = None
    html = None
    form = None
    title = None

    # initialize state
    try:
        # get the state if available
        counter = int(args.get("state")) + 1
    except:
        # initialize the state
        counter = 1

    output = USAGE
    state = str(counter)    
    input_value = args.get("input", "")

    # Check if this is from a form submission
    if type(input_value) is dict and "form" in input_value:
        data = input_value["form"]
        output = "FORM:\n"
        for field in data.keys():
          output += f"{field}: {data[field]}\n"
    elif input_value == "":
        output = f"Welcome to the Demo chat. {USAGE}"
    elif input_value == "code":
        code = CODE
        language = "python"
        output = f"Here is some python code.\n```python\n{code}\n```"
    elif input_value == "html":
        html = HTML
        output = f"Here is some HTML.\n```html\n{html}\n```"
    elif input_value == "message":
        message = "This is the message."
        title = "This is the title"
        output = "Here is a sample message."
    elif input_value == "form":
        output = "please fill the form"
        form = FORM
    elif input_value == "chess":
        chess = CHESS
        output = f"Check this chess position.\n\n{chess}"
    elif input_value == "options":
        output = json.dumps({"options": ["who are you", "what can you do"]})
    # Handle option button clicks - add responses for the specific options
    elif input_value == "who are you":
        output = "I am a demo bot that can show you different types of content. I can display code, chess positions, HTML forms, and messages. Try typing 'options' to see what I can do!"
    elif input_value == "what can you do":
        output = f"I can show you various types of content:\n- 'code': Display Python code examples\n- 'chess': Show chess positions\n- 'html': Display HTML forms\n- 'form': Show interactive forms\n- 'message': Display sample messages\n- 'options': Show option buttons\n\n{USAGE}"
    else:
        output = f"You made {counter} requests. {USAGE}"
    
    # state is a counter incremented at any invocation
    res = {
        "output": output,
    }

    if state: res['state'] = state
    if language: res['language'] = language
    if message: res['message'] = message     
    if title: res['title'] = title
    if chess: res['chess'] = chess
    if code: res['code'] = code
    if html: res['html'] = html
    if form: res['form'] = form

    return res