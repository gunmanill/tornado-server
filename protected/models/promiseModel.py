from baseModel import BaseModel
import re
from tornado import gen
from config import promise_file
from logModel import LogModel
from userModel import UserModel

class PromiseModel(BaseModel):

	@staticmethod
	@gen.coroutine
	def createPromise(user_id):
		yield PromiseModel.sql('INSERT INTO "promises" (user_id) VALUES (%s)', user_id)

	@staticmethod
	@gen.coroutine
	def insertCommands(commands):
		yield PromiseModel.sql('UPDATE "promises" SET status=\'edit\', promise = promise || %s', commands)

	@staticmethod
	@gen.coroutine
	def addUser(node_id, access = ''):
		command = ''
		yield PromiseModel.insertCommands(command)
		

	@staticmethod
	@gen.coroutine
	def addUserOnClass(class_id, access = ''):
		command = ''
		yield PromiseModel.insertCommands(command)

	@staticmethod
	@gen.coroutine
	def dumpPromise(user_id):
		promise = yield PromiseModel.sql('UPDATE "promises" SET status=\'queued\' WHERE user_id=%s RETURNING *')
		user = yield UserModel.getUser(user_id)
		LogModel.write('promise', user[0]['name'], 'dump', None, promise[0]['promise'])
		yield PromiseModel.createPromise(user_id)
		

	@staticmethod
	@gen.coroutine
	def checkForCompleate():

		if 0:
			status = 'compleate'

			promise = yield PromiseModel.sql('UPDATE "promises" SET status=\'complete\' WHERE status=\'dumped\' RETURNING *')
			user = yield UserModel.getUser(promise[0]['user_id'])
			LogModel.write('promise', user[0]['name'], status, None, promise[0]['promise'])

			ret = yield PromiseModel.sql('UPDATE "promises" SET status=\'dumped\' WHERE id=(SELECT id FROM "promises" WHERE status=\'queued\' ORDER BY created ASC LIMIT 1) RETURNING *')
			if ret:
				f2 = open(promise_file, "w")
				f2.write(ret[0]['promise'])
				f2.close()

	@staticmethod
	@gen.coroutine
	def getPromises():