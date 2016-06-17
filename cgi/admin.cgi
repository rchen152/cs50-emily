#!/usr/bin/python

# Import the CGI module
import cgi
import crypt
import random
import string
import sys
import emily

# Required header that tells the browser how to render the HTML.
print 'Content-Type: text/html\n\n'

def generate_login_form():
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
      <div id="login-area">
        <span class="info-text" style="margin-left: 40px;">Admin Login</span>
        <br /><br />
        <form name="reply" method="post" action="admin.cgi" autocomplete="off">
          <span class="login-label">Username</span>
          <input class="login" type="text" name="username" autofocus="autofocus" />
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
          <script>
            $(function() {$('[autofocus]').focus()});
          </script>
          <br /><br />
          <span class="login-label">Password</span>
          <input class="login" type="password" name="password" />
          <input type="hidden" name="action" value="display" />
          <br /><br />
          <input id="login-submit" class="button" type="submit" value="Log in" />
        </form>
      </div>
    </body>
  </html>
  '''

def test(id, passwd):
  passwd_file = open('passwords.txt', 'r')
  line = passwd_file.readline()
  passwd_file.close()
  combo = line.split(':')
  encrypted_pw = crypt.crypt(passwd, combo[1])
  if id == combo[0] and encrypted_pw[:13] == combo[1][:13]:
    return 'passed'
  return 'failed'

def create_session(id):
  session_file = open('sessions.txt', 'a')
  session_key = random_key(8)
  session_file.write(session_key + ':' + id+'\n')
  session_file.close()
  return session_key

def fetch_username(key):
  session_file = open('sessions.txt', 'r')
  lines = session_file.readlines()
  session_file.close()
  for line in lines:
    pair = line.split(':')
    if pair[0] == key:
      return pair[1].rstrip('\n')
  return None

def delete_session(key):
  session_file = open('sessions.txt', 'r')
  lines = session_file.readlines()
  session_file.close()

  session_file = open('sessions.txt', 'w')
  for line in lines:
    pair = line.split(':')
    if not pair[0] == key:
      session_file.write(line)
  session_file.close()

def random_key(length):
  key = ''
  for i in xrange(length):
    key = key + random.choice(string.lowercase + string.uppercase + string.digits)
  return key

def display_page(result, id, session_key = 0):
  if result=='passed':
    if session_key == 0:
      session_key = create_session(id)
    responses = emily.get_all_responses()
    length = len(responses)
    print '''<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="style.css" type="text/css" />
    <title>Emily</title>
  </head>
  <body>
    <div id="right-bar">
      <img src="emily-small.png" alt="Teach Emily" />
    </div>
    <div id="header">
      <img src="logo.png" alt="Home" />
    </div>
    <div id="conversation-area">
      <form method="post" action="admin.cgi">
        <select name="response-select" class="admin-select" size="20">'''
    for i in xrange(length):
      print '\t\t  <option value=' + str(length-i-1) + '>' + str(length-i-1) + ': ' + responses[i] + '</option>\n'
    print '''\t\t</select>
        <br /><br />
        <input type="hidden" name="session_key" value='''+session_key+''' />
        <input type="submit" name="response-delete" class="button" value="Delete." />
      </form>
      <br />
      <form method="post" action="admin.cgi">
        <input type="hidden" name="session_key" value='''+session_key+''' />
        <input type="hidden" name="logout" value="logout" />
        <input type="submit" class="button" value="Logout." />
      </form>
    </div>
  </body>
</html>'''
  else:
    generate_login_form()

def main():
  form = cgi.FieldStorage()
  if 'session_key' in form:
    if 'logout' in form:
      delete_session(form['session_key'].value)
      generate_login_form()
    else:
      if 'response-delete' in form:
        if 'response-select' in form:
          emily.delete_response(index=int(form['response-select'].value))
      u_id = fetch_username(form['session_key'].value)
      display_page('passed', u_id, form['session_key'].value)
  elif 'action' in form and 'username' in form and 'password' in form:
    if form['action'].value == 'display':
      result = test(form['username'].value, form['password'].value)
      display_page(result, form['username'].value)
  else:
    generate_login_form()

main()
