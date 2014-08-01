from baseHandler import BaseHandler
from time import time
from time import sleep
from userModel import UserModel
from config import max_login_try_count
import tornado.web
from config import session_expires


class LoginHandler(BaseHandler):

		
	@tornado.gen.coroutine
	def _get(self, login = '', error = False):
		if self.current_user:
			self.redirect('/')
			
			return

		self.set_secure_cookie('render_time', str(time()))
		attempts = yield UserModel.getAttempts(self.request.remote_ip)
		if not attempts:
			attempts = 0
		else:
			attempts = attempts[0]['attempts']
		self.render('login.html', **{'error' : error, 
									'try_count' : max_login_try_count - attempts, 
									'login' : login})
		
	

	@tornado.gen.coroutine
	def _post(self):

		if not self.get_secure_cookie('render_time'):
			self.write('Error : You browser doesn\'t suppot cookies');
			self.finish()
			return

		
		ip = self.request.remote_ip

		if time() - float(self.get_secure_cookie('render_time')) < 1:
			yield UserModel.banIp(ip)
			self.write('Error : your ip is now blocked')
			self.finish()
			return

		if self.current_user:
			self.redirect('/')
			
			return

		ret = yield UserModel.login(self.get_argument('login'), 
									self.get_argument('password'))

		if ret:
			yield UserModel.delAttempts(ip)
			self.set_secure_cookie(name = 'user', value = tornado.escape.json_encode(ret[0]), expires = time() + 60*session_expires)
			self.redirect('/')
			
			return

		yield UserModel.increaseAttempts(ip)

		yield self._get(self.get_argument('login'), True)

	