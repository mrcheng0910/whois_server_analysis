import math
import sys
import os
import re
import time
import datetime

def ping(ip, count = 10):
	res = os.popen("ping " + ip + " -c " + str(count))
	resLst = list(res)
	print resLst

	lossPattern = re.compile(r".+? ([\d\.]+)%")
	loss = 0
	for i in resLst:
		info = lossPattern.findall(i)
		if info:
			loss = float(info[0]) 
			break

	timePattern = re.compile(r'.+?time=(.+) .*s')
	timeLst = []
	for i in resLst:
		info = timePattern.findall(i)
		if info:
			timeLst.append(float(info[0]))
	num = len(timeLst)
	if num == 0:
		return loss, 100, 0
	mean = sum(timeLst) / num
	tmp = 0
	for i in timeLst:
		tmp += (i - mean) * (i - mean)
	if num != 1:
		variance = math.sqrt(tmp) / (num - 1)
	else:
		variance = 0

	return loss, mean, variance

def traceroute(ip):
	res = os.popen("traceroute " + ip)
	resLst = list(res)
	print resLst

	num = 0
	for i in resLst:
		i = i.strip()
		try:
			int(i[0])
			num += 1
		except:
			continue
	return num

if __name__ == "__main__":
	i = 0
	while i < 10:
		with open(sys.argv[1], "r") as fin:
			for line in fin:
				ip = line.strip()
				try:
					loss, delay, var = ping(ip)	
				except:
					loss, delay, var = 100, 100, 0
				try:
					pathLen = traceroute(ip)
				except:
					pathLen = 100
				print loss, delay, var, pathLen
				new=str(datetime.datetime.now())[:19]
				with open(sys.argv[2], "a") as fout:
					fout.write(ip + " %.2f %.2f %.2f %d %s\n" % (loss, delay, var,  pathLen, new) )
			i += 1
			time.sleep(1)

	
