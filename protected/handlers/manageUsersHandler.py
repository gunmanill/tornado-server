from baseHandler import BaseHandler
import tornado.web
import utils

from userModel import UserModel
from nodeModel import NodeModel

class ManageUsersHandler(BaseHandler):

	@tornado.gen.coroutine
	def _get(self, 
			userDescription = '', 
			userLogin = '', 
			userPassword = '', 
			userPassword2 = '', 
			userKey = '', 
			interfaceAccess = False, 
			error = False,
			nodeUserAccessList = [],
			nodeSudoAccessList = [],
			classUserAccessList = [],
			classSudoAccessList = []):
		
		users = yield UserModel.getUsers()
		nodes = yield NodeModel.getNodes()
		nodesById = {}
		for node in nodes:
			nodesById.update({node['id'] : utils.toDict(node)})
		classes = yield NodeModel.getClasses()
		classesById = {}
		for cl in classes:
			classesById.update({cl['id'] : utils.toDict(cl)})


		self.render('manage-users.html', **{'error' : error, 
											'users' : users, 
											'userKey' : userKey, 
											'interfaceAccess' : interfaceAccess, 
											'userDescription' : userDescription, 
											'userLogin' : userLogin, 
											'userPassword' : userPassword, 
											'userPassword2' : userPassword2,
											'nodesById' : nodesById,
											'classesById' : classesById,
											'nodeUserAccessList' : nodeUserAccessList,
											'nodeSudoAccessList' : nodeSudoAccessList,
											'classUserAccessList' : classUserAccessList,
											'classSudoAccessList' : classSudoAccessList
											})

	@tornado.gen.coroutine
	def _post(self):

		key = tornado.escape.xhtml_unescape(self.get_argument('userKey'))
		ia = False
		if 'interfaceAccess' in self.request.arguments.keys():
			ia = True

		nodeUserAccessList = []
		nodeSudoAccessList = []
		classUserAccessList = []
		classSudoAccessList = []



		if 'nodeUserAccessList' in self.request.arguments.keys():
			nodeUserAccessList = self.request.arguments['nodeUserAccessList']
		if 'nodeSudoAccessList' in self.request.arguments.keys():
			nodeSudoAccessList = self.request.arguments['nodeSudoAccessList']
		if 'classUserAccessList' in self.request.arguments.keys():
			classUserAccessList = self.request.arguments['classUserAccessList']
		if 'classSudoAccessList' in self.request.arguments.keys():
			classSudoAccessList = self.request.arguments['classSudoAccessList']
		
		if self.get_argument('action') == 'add':
			error = yield UserModel.addUser(self.get_argument('userLogin'), 
											self.get_argument('userPassword'), 
											self.get_argument('userPassword2'), 
											ia, 
											self.get_argument('userDescription'), 
											key,
											nodeUserAccessList,
											nodeSudoAccessList,
											classUserAccessList,
											classSudoAccessList)

		elif self.get_argument('action') == 'save':
			error = yield UserModel.updateUser(self.get_argument('userId'), 
												self.get_argument('userLogin'), 
												self.get_argument('userPassword'), 
												self.get_argument('userPassword2'), 
												ia, 
												self.get_argument('userDescription'), 
												key,
												nodeUserAccessList,
												nodeSudoAccessList,
												classUserAccessList,
												classSudoAccessList)
		elif self.get_argument('action') == 'delete':
			error = yield UserModel.deleteUser(self.get_argument('userId'))

		if not error:
			yield self._get();
		else:
			yield self._get(self.get_argument('userDescription'), 
							self.get_argument('userLogin'), 
							self.get_argument('userPassword'), 
							self.get_argument('userPassword2'), 
							key, 
							ia, 
							error,
							nodeUserAccessList,
							nodeSudoAccessList,
							classUserAccessList,
							classSudoAccessList
							)