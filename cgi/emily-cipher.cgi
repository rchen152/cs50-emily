#!/usr/bin/python

# Import the CGI module
import cgi
import re

questions = ['What is the cleverest cipher in the world?',
      'Precisely. What would you like to know about?',
      'They\'re in my picture.']
answers = {questions[0] : r'rot-?13',
           questions[1] : r'sweets',
           questions[2] : None}

# The Cookie
print 'Set-Cookie: thecookie=nomnom'
# Required header that tells the browser how to render the HTML.
print 'Content-Type: text/html\n\n'

def generate_form(conversation = questions[0] + '\n'):
  print '''<!DOCTYPE html>
  <html>
    <head>
      <link rel="stylesheet" href="style.css" type="text/css" />
      <title>Emily</title>
    </head>
    <body>
      <div id="right-bar">
        <a href="vault.cgi"><img src="emily-small-cipher.png" alt="Emily" /></a>
      </div>
      <div id="header">
        <a href="emily-cipher.cgi"><img src="logo.png" alt="Home" /></a>
      </div>
      <div id="conversation-area">
        <form name="reply" method="post" action="emily-cipher.cgi" autocomplete="off">
          <textarea name="conversation-text" id="conversation-text" readonly="readonly" rows="20">'''+conversation+'''</textarea>
          <!-- Sweets. Definitely sweets.-->
          <script>
            var textarea = document.getElementById('conversation-text');
            textarea.scrollTop = textarea.scrollHeight;
          </script>
          <br /><br />
          <input type="text" name="user-response" id="user-response" autofocus="autofocus" />
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
          <script>
            $(function() {$('[autofocus]').focus()});
          </script>
          <br /><br />
          <input type="submit" id="reply-button" class="button" value="Reply" />
          <br /><br />
        </form>
      </div>
    </body>
  </html>
  '''

def emily_says(line0, line1):
  answer = answers.get(line0.strip(), None)
  if answer == None:
    return line0.strip()
  return (questions[(questions.index(line0.strip()) + 1) % len(questions)]
          if re.search(answer,line1.strip(),re.IGNORECASE) else line0.strip())

def main():
  form = cgi.FieldStorage()
  if 'conversation-text' in form:
    if 'user-response' in form:
      conversation = form['conversation-text'].value
      lines = conversation.split('\n')
      line0 = lines.pop()
      while len(line0) < 1 or not line0[0].isalnum():
        line0 = lines.pop()
      line1 = form['user-response'].value
      generate_form(
        conversation + line1 + '\n\n' + emily_says(line0, line1) + '\n')
    else:
        generate_form(form['conversation-text'].value)
  else:
    generate_form()

main()
