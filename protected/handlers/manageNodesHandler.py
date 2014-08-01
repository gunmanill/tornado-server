from baseHandler import BaseHandler
import tornado.web
from nodeModel import NodeModel

class ManageNodesHandler(BaseHandler):

	@tornado.gen.coroutine
	def _get(self, nodeName = '', nodeIp = ('', '', '', ''), error = False):
		
		nodes = yield NodeModel.getNodes()
		self.render('manage-nodes.html', **{'nodes' : nodes, 
											'nodeName' :nodeName, 
											'nodeIp' : nodeIp, 
											'error' : error})

	@tornado.gen.coroutine
	def _post(self):

		nodeIp = '.'.join(self.request.arguments['nodeIp'])
		
		if self.get_argument('action') == 'add':
			error = yield NodeModel.addNode(self.get_argument('nodeName'), nodeIp)
		elif self.get_argument('action') == 'save':
			error = yield NodeModel.updateNode(self.get_argument('nodeId'), 
												self.get_argument('nodeName'), 
												nodeIp)
		elif self.get_argument('action') == 'delete':
			error = yield NodeModel.deleteNode(self.get_argument('nodeId'))
		
		yield self._get(self.get_argument('nodeName'), 
						self.request.arguments['nodeIp'], 
						error)
