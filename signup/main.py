#!/usr/bin/env python
import webapp2
import re

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)

def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)

def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return EMAIL_RE.match(email)

form="""
<html>
  <head>
    <title>Sign Up - Nitin</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(username_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(password_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(verify_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""    

class WelcomeHandler(webapp2.RequestHandler):
        def get(self):
            username = self.request.get("username")
            self.response.out.write("Welcome, %s!" % (username))

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", email="", 
        username_error="", password_error="", verify_error="", email_error=""):
        self.response.out.write(form % {"username": username,
                                        "email": email,
                                        "username_error": username_error,
                                        "password_error": password_error,
                                        "verify_error": verify_error,
                                        "email_error": email_error})
    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""
        check_username = valid_username(user_username)
        check_password = valid_password(user_password)
        check_email = valid_email(user_email)

        if user_username and check_username and user_password and check_password and user_verify == user_password and ((user_email and check_email) or (not user_email)):
            self.redirect("/Welcome?username=" + user_username)
        else:
            if not user_username or not check_username:
                username_error = "That's not a valid username."
            if not user_password or not check_password:
                password_error = "That wasn't a valid password."
            elif user_password and user_verify != user_password:
                verify_error = "Your passwords didn't match."
            if user_email and not check_email:
                email_error = "That's not a valid email."
            self.write_form(user_username, user_email, username_error, password_error, verify_error, email_error)

    
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/Welcome', WelcomeHandler)
], debug=True)
