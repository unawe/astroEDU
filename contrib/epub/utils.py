import re

def extract_title(content):
	title = None
	level = 0
	#f = open(content)
	#html = f.read().decode('utf8')
	#f.close()
	#m = re.search('<h[123]>(.*)</h([123])>', html)
	m = re.search('<h[123].*?>(.*)</h([123])>', content)
	if m:
		title = m.group(1)
		level = m.group(2)
		title = title.replace('<br/><br/>', ' - ')
		title = title.replace('<br/>', ' ')
		title = re.sub('<.*?>', '', title)
		# title = re.sub('<a[^>]*>[^<]*</a>', '', title)
		# title = re.sub('</?i>', '', title)

	return title, level

def append_toc(toc, file_id, title, href, level):
	parentlist = None
	if level == '1':
		parentlist = toc
	elif level == '2':
		parentlist = toc[-1]['children']
	elif level == '3':
		if len(toc[-1]['children']) == 0:
			toc[-1]['children'].append({'id':None, 'title':None, 'href':None, 'children':[]})
		parentlist = toc[-1]['children'][-1]['children']
	#print '>', level, title
	parentlist.append({'id':file_id, 'title':title, 'href':href, 'children':[]})

def toc_html(toc, level=0):
	result = ''
	level += 1
	for e in toc:
		if e['title']:
			item = '<a href="%s">%s</a>' % (e['href'], e['title'])
			item += toc_html(e['children'], level)
			item = '\n<li>%s</li>' % item
			result += item
		else:
			result = toc_html(e['children'], level)
	if result:
		result = '<ul class="level_%d">%s</ul>' % (level, result)
	return result
