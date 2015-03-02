#!/path/to/python3.4
# -*- coding: utf-8 -*-

import cgi
import cgitb
import io
import json
import os
import sys

def main():
	cgitb.enable()
	
	query = cgi.parse_qs(os.environ['QUERY_STRING'])
	refs = open('references.json', encoding='utf-8').read()
	refs = json.loads(refs)
	checklist = [
		('title', lambda x: x),
		('author', lambda x: ' and '.join(x)),
		('journal', lambda x: x),
		('booktitle', lambda x: x),
		('publisher', lambda x: x),
		('address', lambda x: x),
		('pages', lambda x: str(x) if len(x) == 1 else str(x[0])+'--'+str(x[1])),
		('month', lambda x: str(x)),
		('year', lambda x: str(x)),
	]
	
	if 'name' in query:
		print('Content-Type: text/plain; charset=UTF-8')
		print()
		name = query['name'][0]
		if name in refs:
			name = query['name'][0]
			ref = refs[name]
			info = []
			print('@%s {%s,' % (ref['type'], name))
			for k, f in checklist:
				if k in ref:
					info.append('  %s = {%s}' % (k, f(ref[k])))
			print(',\n'.join(info))
			print('}')
		else:
			print('No reference')
	else:
		print('Content-Type: text/html; charset=UTF-8')
		print()
		print('<html><head><title>References</title></head><body><ul>')
		for k in sorted(refs.keys(), reverse=True):
			print('<li><a href="/bibtex.cgi?name=%s" target="_blank">%s</a></li>' % (k, k))
		print('</ul></body></html>')

if __name__ == '__main__':
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
	main()
