import web
import os
from jinja2 import Environment,FileSystemLoader
#from jinja2_markdown.extensions import MarkdownExtension

urls = (
  '/', 'index',
  '/tdiary', 'tdiary'
)

app = web.application(urls, globals())
application = app.wsgifunc()

def render_template(template_name, **context):
	extensions = context.pop('extensions', [])
	globals = context.pop('globals', {})
	
	jinja_env = Environment(
		loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
		extensions=extensions,
		)
	jinja_env.globals.update(globals)
	
	#jinja_env.update_template_context(context)
	return jinja_env.get_template(template_name).render(context)

class index:
        def GET(self):
                #return render_template('index.html', extensions=[MarkdownExtension])
                return render_template('index.html')

class tdiary:
        def GET(self):
                return render_template('tlist.html')

class hello:
	def GET(self):
		return render_template('layout.html', name='world', )

if __name__ == "__main__": app.run()
	
