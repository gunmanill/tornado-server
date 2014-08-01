from baseHandler import BaseHandler
import tornado.web
from logModel import LogModel
import utils
import datetime

class WatchLogHandler(BaseHandler):

	@tornado.gen.coroutine
	def _get(self):
		self.render('watch-log.html')

	@tornado.gen.coroutine
	def _post(self):
		ret = yield LogModel.getLogFromTimeStamp(self.get_argument('timestamp'), self.get_argument('order'), self.get_argument('desc'))
		
		self.write(tornado.escape.json_encode(utils.arrToDic(ret)))
		self.finish()
		