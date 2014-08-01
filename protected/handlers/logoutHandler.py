from baseHandler import BaseHandler
import tornado.web

class LogoutHandler(BaseHandler):

	@tornado.gen.coroutine
	def _get(self):
		self.clear_cookie('user')
		self.redirect('/login')
