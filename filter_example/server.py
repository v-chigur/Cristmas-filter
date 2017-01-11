import tornado.ioloop
import tornado.web
import random
import os, uuid
from filter import process

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		fname = self.get_argument('im', 'default')
		if fname=='default':
			cname = str(uuid.uuid4())
			self.render('upload.html', name = cname)
		else:
			fnames = listdir('results')
			self.render('result.html', name = fname)
	def post(self):
		fileinfo = self.request.files['image'][0]
		fname = fileinfo['filename']
		extn = os.path.splitext(fname)[1]
		cname = str(uuid.uuid4()) + extn
		fh = open('images/' + cname, 'wb')
		fh.write(fileinfo['body'])

		process('images/' + cname, 'results/' + cname)
		self.render('result.html', name = cname)

settings = [
	('/', MainHandler),
	('/results/(.*)', tornado.web.StaticFileHandler, {'path': 'results'})
]

app = tornado.web.Application(settings) #web server object
app.listen(8888)
tornado.ioloop.IOLoop.current().start() #make program not to stop