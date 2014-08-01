import os

app_dir = os.path.abspath(os.path.dirname(__file__)) + '/'
handler_dir = app_dir + 'handlers/'
model_dir = app_dir + 'models/'
view_dir = app_dir + 'views/'

db = {
	'dsn' : 'host=localhost port=5432 dbname=veevavoo user=veevavoo password=oovaveev',
	'size' : 1,
	'max_size' : 3,
	'setsession' : ("SET TIME ZONE UTC",),
	'raise_connect_errors' : False,
}

max_login_try_count = 10

port = 8888

md5_salt = '#2jb9234)(KSFew@8jncsUDHi7'

session_expires = 20

settings = {
    'cookie_secret' : 'jkdsk#e209uhJKLaSJDHfeh23r2dsn1WSDJhn3;s',
    'login_url' : '/login',
    'xsrf_cookies' : True,
    'template_path' : view_dir
}

promise_file = app_dir + 'test_file.cr'
promise_log = ''
promise_check_time = 30 #seconds