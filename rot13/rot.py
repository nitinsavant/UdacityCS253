import cgi
import codecs

def escape_html(s):
	return cgi.escape(s, quote=True)

def rot13(s):
	return codecs.encode(s, 'rot_13')