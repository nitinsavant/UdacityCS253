import os
import jinja2
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

# Permalink page for each submission. Upon GET request, the post_id is retrieved from 
# the regex in the URL and if the post_id exists, the permalink page is displayed.
class PostHandler(Handler):
    def get(self, post_id):
        p = Post.get_by_id(int(post_id))
        if p:
            self.render("post_perma.html", p = p)

# Main blog page. It only accepts GET and displays all blog posts stored in database.        
class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        self.render("blog_main.html", posts = posts)

# New Post page. Accepts submissions via POST. If error, it displays message and 
# maintains content. If successful, the submission is stored (i.e put) in database 
# and user is redirected to the submission'spermalink page. If unsucessful, error 
# message is displayed and NewPost form is re-rendered with submitted data.
class NewPost(Handler):
    def render_post(self, subject="", content="", error=""):
        self.render("newpost.html", subject = subject, content = content, error = error)

    def get(self):
        self.render('newpost.html')

    def post(self):
        content = self.request.get("content")
        subject = self.request.get("subject")

        if content and subject:
            a = Post(subject = subject, content = content)
            a.put()
            x = str(a.key().id())
            self.redirect("/%s" %x)
        else:
            error = "We need both a title and a post!"
            self.render_post(subject, content, error)

app = webapp2.WSGIApplication([
    ('/', MainPage), 
    ('/newpost', NewPost),
    ('/([0-9]+)', PostHandler)
], debug=True)
