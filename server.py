import tornado.ioloop
import tornado.web
import random

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<form method='get' action='/hello'><input name='name' /></form>")

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		name = self.get_argument("name", "Анон")
		self.write("<h1>Привет, " + name + "!</h1>")

class CatsHandler(tornado.web.RequestHandler):
	def get(self):
		cats = [
			('Васька', 'http://content.foto.mail.ru/mail/slada-la/_blogs/i-290.jpg'),
			('Петька', 'http://cs418625.vk.me/v418625196/7958/hMyCsq2Lmdg.jpg'),
			('Хлоя', 'http://cs8.pikabu.ru/post_img/big/2016/01/18/3/1453088963189484452.jpg')
		]
		cat = random.choice(cats)
		self.render("cats.html", cat_name = cat[0], cat_adress = cat[1])

settings = [
	('/', MainHandler),
	('/hello', HelloHandler),
	('/cats', CatsHandler),
	('/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'})
]
#http://host:port/page/?param1=value1&param2=value2

app = tornado.web.Application(settings) #web server object
app.listen(8888)
tornado.ioloop.IOLoop.current().start() #make program not to stop