#!/usr/bin/python

# Import the CGI module
import cgi
import emily

default_start = emily.start_conversation()

# Required header that tells the browser how to render the HTML.
print 'Content-Type: text/html\n\n'

def generate_form(conversation = 'Emily: ' + default_start, suggestions = ''):
  print '''<!DOCTYPE html>
  <html>
    <head>
      <link rel="stylesheet" href="style.css" type="text/css" />
      <title>Emily</title>
    </head>
    <body>
      <form name="reply" method="post" action="brain.cgi" autocomplete="off">
        <div id="right-bar">
          <textarea id="instructions" class="right-element info-text" readonly="readonly">Please teach me about the outside world.  When I don't know how to reply to something, compose my reply for me, press enter, then type your response.  Below will display all suggestions within my memory.</textarea>
          <br /><br />
          <textarea name="suggestions" id="suggestions" class="right-element" readonly="readonly">'''+suggestions+'''</textarea>
        </div>
        <div id="header">
          <a href="emily.cgi"><img src="logo.png" alt="Home" /></a>
        </div>
        <div id="conversation-area">
          <textarea name="conversation-text" id="conversation-text" readonly="readonly" rows="20">'''+conversation+'''</textarea>
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
          <input type="submit" class="button" id="reply-button" value="Reply" />
        </div>
      </form>
    </body>
  </html>
  '''

def main():
  form = cgi.FieldStorage()
  if 'conversation-text' in form:
    if 'user-response' in form:
      conversation = form['conversation-text'].value
      lines = conversation.split('\n')
      line_0 = lines.pop()
      while len(line_0) < 1 or not line_0[0].isalnum():
        line_0 = lines.pop()
      ind = line_0.find('Emily: ')
      if ind == 0:
        line_0 = line_0[7:]
        line_1 = form['user-response'].value
        next = emily.say(line_0, line_1, teaching=True)
        if not next == None:
          suggestions = emily.get_user_responses(next)
          generate_form(conversation + 'You: ' + line_1 + '\n\n' + 'Emily: ' + next, make_text(suggestions))
        else:
          suggestions = emily.get_emily_responses(line_0, line_1)
          generate_form(conversation + 'You: ' + line_1 + '\n\n', make_text(suggestions))
      else:
        line_2 = form['user-response'].value
        line_1 = line_0
        line_0 = lines.pop()
        while len(line_0) < 1 or not line_0[0].isalnum():
          line_0 = lines.pop()
        emily.teach(line_0[7:], line_1[5:], line_2)
        suggestions = emily.get_user_responses(line_2)
        generate_form(conversation + 'Emily: ' + line_2 + '\n', make_text(suggestions))
    else:
        generate_form(form['conversation-text'].value, form['suggestions'].value)
  else:
    suggestions = emily.get_user_responses(default_start)
    generate_form(suggestions = make_text(suggestions))

def make_text(ltext = []):
  text = ''
  for line in ltext:
    text = text + line + '\n'
  return text

main()
