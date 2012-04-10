import web
import os
import time
from jinja2 import Environment,FileSystemLoader
#from jinja2_markdown.extensions import MarkdownExtension

urls = (
  '/', 'index',
  '/tdiary', 'tdiary',
  '/tadd', 'tadd',
)

#web.config.debug = False

app = web.application(urls, globals())
application = app.wsgifunc()

db = web.database(dbn='sqlite', db='basic_training.db')

def render_template(template_name, **context):
  extensions = context.pop('extensions', [])
  globals = context.pop('globals', {})
    
  jinja_env = Environment(
  loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
  extensions=extensions,
  )
  jinja_env.globals.update(globals)
    
  jinja_env.filters['datetimeformat'] = datetimeformat
    
  #jinja_env.update_template_context(context)
  return jinja_env.get_template(template_name).render(context)

def datetimeformat(value, format='%d.%m.%Y'):
  return value.strftime(format)

class index:
  def GET(self):
    #return render_template('index.html', extensions=[MarkdownExtension])
    return render_template('index.html')

class tdiary:
  def GET(self):
    trainings = db.select('basic_training', what="title,traindate,tt,avp,mxp,z1,z2,z3,avs,dst,kcal,author_description,route", order="traindate ASC").list()
    
    return render_template('tlist.html', tlist=trainings)

class tadd:
  def GET(self):
    return render_template('tadd.html', path=web.ctx.path)

  def POST(self):
    i = web.input()

    id = db.insert(
        'basic_training',
        title=i.title,
        traindate=time.strftime('%Y-%m-%d',(time.strptime(i.traindate, '%d.%m.%Y'))),
        tt=i.traintime,
        avp=i.avp,
        mxp=i.mxp,
        z1=i.hz,
        z2=i.fz,
        z3=i.pz,
        avs=i.avs,
        dst=i.dst,
        kcal=i.kcal,
        author_description='No Desc',
        route=i.route)

    print i, id

    raise web.seeother('/tdiary')

class hello:
	def GET(self):
		return render_template('layout.html', name='world', )

if __name__ == "__main__": app.run()

