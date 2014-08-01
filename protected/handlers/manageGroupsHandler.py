from baseHandler import BaseHandler
import tornado.web

from nodeModel import NodeModel

class ManageGroupsHandler(BaseHandler):

	@tornado.gen.coroutine
	def _get(self, className = '', error = False):

		classes = yield NodeModel.getClasses()
		
		nodes = yield NodeModel.getNodes()
		nodesById = {}
		for node in nodes:
			nj = {}
			for key, value in node.items():
				nj.update({key : value})
			nodesById.update({node['id'] : nj})
		self.render('manage-groups.html', **{'classes' : classes, 
											'className' : className, 
											'error' : error, 
											'nodesById' : nodesById})

	@tornado.gen.coroutine
	def _post(self):

		if not ('classList' in self.request.arguments.keys()):
			clList = []
		else:
			clList = self.request.arguments['classList']

		if self.get_argument('action') == 'add':
			error = yield NodeModel.addClass(self.get_argument('className'))
		elif self.get_argument('action') == 'save':
			error = yield NodeModel.updateClass(self.get_argument('classId'), 
												self.get_argument('className'), 
												clList)
		elif self.get_argument('action') == 'delete':
			error = yield NodeModel.deleteClass(self.get_argument('classId'))

		yield self._get(self.get_argument('className'), error)