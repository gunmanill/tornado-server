def ipToInt(ip):
	return reduce(lambda a,b: a<<8 | b, map(int, ip.split(".")))

def toDict(t):
	ret = {}
	for key, value in t.items():
		ret.update({key : value})
	return ret

def arrToDic(arr):
	ret = []
	for item in arr:
		ret.append(toDict(item))
	return ret