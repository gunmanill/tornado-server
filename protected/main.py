import config
import imp
import tornado.web
import tornado.httpserver
import tornado.ioloop
import sys

from tornado.options import define, options

sys.path.append(config.handler_dir)
sys.path.append(config.model_dir)

from loginHandler import LoginHandler
from manageUsersHandler import ManageUsersHandler
from logoutHandler import LogoutHandler
from manageNodesHandler import ManageNodesHandler
from manageGroupsHandler import ManageGroupsHandler
from watchLogHandler import WatchLogHandler
from promiseModel import PromiseModel

define('port', default = config.port, help = 'run on the given port', type = int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'^/', ManageUsersHandler),
			(r'^/manage-nodes$', ManageNodesHandler),
			(r'^/login$', LoginHandler),
			(r'^/logout$', LogoutHandler),
			(r'^/manage-groups$', ManageGroupsHandler),
			(r'^/watch-log$', WatchLogHandler),
		]

		tornado.web.Application.__init__(self, handlers, **config.settings)


def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	main_loop = tornado.ioloop.IOLoop.instance()
	scheduler = tornado.ioloop.PeriodicCallback(PromiseModel.checkForCompleate, config.promise_check_time * 1000, io_loop = main_loop)
	
	scheduler.start()
	main_loop.start()

if __name__ == "__main__":
    main()