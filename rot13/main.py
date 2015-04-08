#!/usr/bin/env python
import webapp2
import rot

form="""
<html>
<head>
    <title>Nitin Savant - Unit 2 Rot 13</title>
</head>
<body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
        <textarea name="text" style="height: 100px; width: 400px;">%(data)s</textarea>
    <br>
    <input type="submit">
    <div style="color: blue">%(message)s</div>
    </form>
</body>
</html>
"""    

class MainHandler(webapp2.RequestHandler):
    def write_form(self, message="", data=""):
        self.response.out.write(form % {"message": message,
                                        "data": rot.escape_html(data)})
    def get(self):
        self.write_form()
    def post(self):
        text = self.request.get('text')
        newtext= rot.rot13(text)
        self.write_form("Enjoy your rotted text!", newtext)
    
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
