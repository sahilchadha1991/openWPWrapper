import json
from pprint import pprint

data = {}
data['https://stylestories.ebay.com/'] = 'sachadha@ebay.com'
data['http://www.ebay.com/motors/blog/'] = 'sahilchadha1991@gmail.com'
data['http://retailexport.ebay.cn/'] = 'dude.sahil@gmail.com'
data['http://tech.ebay.com'] = 'securityresearch@ebay.com'
data['http://www.ebay.co.jp/'] = 'dud.esahil@gmail.com'

json_data = json.dumps(data)
print json_data

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

with open('data.txt') as data_file:
    data = json.load(data_file)


for key, val in data.iteritems():
	print key, val
 