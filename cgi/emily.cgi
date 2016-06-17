#!/usr/bin/python

# Import the CGI module
import cgi
import emily

default_start = emily.start_conversation()

# Required header that tells the browser how to render the HTML.
print 'Content-Type: text/html\n\n'

def generate_form(conversation = default_start):
  print '''<!DOCTYPE html>
  <html>
    <head>
      <link rel="stylesheet" href="style.css" type="text/css" />
      <title>Emily</title>
    </head>
    <body>
      <div id="right-bar">
        <a href="brain.cgi"><img src="emily-small.png" alt="Teach Emily" /></a>
      </div>
      <div id="header">
        <a href="emily.cgi"><img src="logo.png" alt="Home" /></a>
      </div>
      <div id="conversation-area">
        <form name="reply" method="post" action="emily.cgi" autocomplete="off">
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
          <input type="submit" id="reply-button" class="button" value="Reply" />
          <br /><br />
        </form>
      </div>
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
      line_1 = form['user-response'].value
      generate_form(conversation + line_1 + '\n\n' + emily.say(line_0, line_1))
    else:
        generate_form(form['conversation-text'].value)
  else:
    generate_form()
main()
