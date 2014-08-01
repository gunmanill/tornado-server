import tornado.web
from userModel import UserModel
from config import max_login_try_count
from time import time
from config import session_expires

class BaseHandler(tornado.web.RequestHandler):

	def get_current_user(self):

		user = self.get_secure_cookie('user')
				
		if not user:
			return None

		self.set_secure_cookie(name = 'user', value = user, expires = time() + 60*session_expires)
		
		return UserModel(tornado.escape.json_decode(user))
		
	
	
	@tornado.gen.coroutine
	@tornado.web.asynchronous
	def get(self):
		if not self.current_user:
			yield self.checkIp()

		if not self.current_user and self.request.uri != '/login':
			self.redirect('/login')
			return
		
		yield self._get()
		

	
	@tornado.gen.coroutine
	@tornado.web.asynchronous
	def post(self):
		if not self.current_user:
			yield self.checkIp()
		if not self.current_user and self.request.uri != '/login':
			self.redirect('/login')
			return

		yield self._post()
		

	@tornado.gen.coroutine
	def checkIp(self):
		
		ip = self.request.remote_ip
		
		attempts = yield UserModel.getAttempts(ip)

		if attempts and attempts[0]['attempts'] >= max_login_try_count:
			raise tornado.web.HTTPError(403)
		elif not attempts:
			yield UserModel.setAttempts(ip, 0)


	@tornado.gen.coroutine
	def _post(self):
		pass

	@tornado.gen.coroutine
	def _get(self):
		pass
