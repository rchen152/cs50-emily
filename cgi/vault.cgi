#!/usr/bin/python

# Import the CGI module
import cgi
import re

# Required header that tells the browser how to render the HTML.
print 'Content-Type: text/html\n\n'

def generate_letter():
  print '''<!DOCTYPE html>
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Marck+Script" />
    </head>
    <body style="background-image: url('paper.jpg'); background-repeat: repeat">
      <h1 style="font-family: 'Marck Script', 'Times New Roman', serif">
Dear Catherine,<br /><br />

Here's wishing you a happy, happy twentieth birthday!  It's hard to believe it's been
six years since we met.  As I was reminded while putting together these puzzles, we've
made a lot of wacky, wonderful memories in that time.  I hope you have many exciting,
eye-opening, silly, inspiring, joyful experiences in the coming months, and please keep
in touch!  I except to have an ever greater pool of ridiculous inside jokes to draw
from in future years.<br /><br />

With love (or wuv),<br />
Rebecca<br /><br />

P.S. Have some cartoon strawberries, just to keep the tone from becoming too serious.
      </h1>
      <img src="strawberry-cartoon-set.png" alt="Catherine" />
    </body>
  </html>'''

def generate_form():
  print '''<!DOCTYPE html>
  <html>
    <head>
      <link rel="stylesheet" href="style.css" type="text/css" />
      <title>Emily</title>
    </head>
    <body>
      <div id="right-bar">
        <img src="padlock.jpg" alt="Padlock" />
      </div>
      <div id="header">
        <a href="emily-cipher.cgi"><img src="logo.png" alt="Home" /></a>
      </div>
      <div id="conversation-area">
        <form name="combination" method="post" action="vault.cgi" autocomplete="off">
          <input type="text" class="combo" name="combo0" maxlength="1" autofocus="autofocus" />
          <input type="text" class="combo" name="combo1" maxlength="1" />
          <input type="text" class="combo" name="combo2" maxlength="1" />
          <input type="text" class="combo" name="combo3" maxlength="1" />
          <input type="text" class="combo" name="combo4" maxlength="1" />
          <input type="text" class="combo" name="combo5" maxlength="1" />
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
          <script>
            $(function() {$('[autofocus]').focus()});
          </script>
          <br /><br />
          <input type="submit" class="button" value="Unlock" />
          <br /><br />
        </form>
      </div>
    </body>
  </html>
  '''

def main():
  form = cgi.FieldStorage()
  combo_lst = ['combo' + str(i) for i in range(6)];
  for k in combo_lst:
    if not k in form:
      generate_form()
      return
  guess = ''.join([form[c].value for c in combo_lst])
  if re.search('^nomnom$', guess, re.IGNORECASE):
    generate_letter()
  else:
    generate_form()

main()
