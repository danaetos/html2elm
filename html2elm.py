from collections import namedtuple
import re
import sys
import argparse

Match = namedtuple('Match',['name','start','type'])
singletons = set(['area','base','br','col','command','embed','hr','img','input','keygen','link','meta','param','source','track','wbr'])

class Node(object):

	def __init__(self,name, start = None, text = None):
		self.name = name
		self.start = start
		self.children = []
		self.classes = []
		self.parent = None
		self.attributes = None		
		self.text = text

	def setText(self,t):
		self.text = t

	def setAttributes(self,attrs):
		self.attributes = attrs

	def setParent(self,p):
		self.parent = p

	def addClass(self,c):
		self.classes.append(c)

	def addChild(self,c):
		self.children.append(c)

	def print(self,n):
		if self.text:
			print('\t'*n + '{} "{}"'.format(self.name,self.text))
		else:
			print('\t'*n + '{}'.format(self.name))
		if self.attributes is not None:
			for (k,v) in self.attributes.items():
				print('\t'*n + '{}: {}'.format(k,', '.join(v)))
		for c in self.children:
			c.print(n+1)

def parseAttributes(text):
	matches = [ m for m in re.finditer(r'[a-z,A-Z]+[\s]?=[\s]?"[^"]*"', text) ]	
	attrs = dict()
	for m in matches:
		tokens = text[m.start(0):m.end(0)].replace('"','').split('=')
		attr_name = tokens[0]
		attr_values = tokens[1].split()
		attrs[attr_name] = attr_values
	return attrs

def format_attr(k,vs):
	result = ''
	if k == 'class':
		tuples = ','.join( '("' + v + '",True)' for v in vs)
		result += 'classList [' + tuples + ']'
	else:
		result += 'attribute ' + '"' + k + '" "' + ' '.join(vs) + '"'
	return result

def format_attrs(attributes):
	result = ''
	if attributes is not None: 
		result += ','.join( format_attr(k,vs) for (k,vs) in attributes.items() )
	return result 

def format_elm(node):
	if node.name == 'text':
		text = node.name + ' ' + '"' + node.text + '"'
	else:
		text = node.name + ' [' + format_attrs(node.attributes) + ']\n [' + '\n,'.join( format_elm(c) for c in node.children)  + ']'
	return text

def parse_tree(html):
	pattern_open = r'<[a-z,A-Z]*[\s|>]'
	pattern_close = r'</[a-z,A-Z]*>'
	matches_open = [ Match(html[m.start(0)+1:m.end(0)-1],m.start(0),'open') for m in re.finditer(pattern_open, html)]
	matches_close = [ Match(html[m.start(0)+2:m.end(0)-1],m.start(0),'close') for m in re.finditer(pattern_close, html)]
	ms = sorted(matches_open + matches_close, key = lambda tup: tup.start)

	for i,m in enumerate(ms):
			
		if i==0:
			current_node = Node(ms[0].name,start=ms[0].start)
			current_node.setAttributes(parseAttributes(html[m.start:html.find('>',m.start)]))
			continue

		text_start = html.find('>',ms[i-1].start)+1
		text_end = m.start
		text = html[text_start:text_end].strip()

		if m.type == 'open':
			if text:
				child = Node('text',start=text_start,text=text)
				current_node.addChild(child)
			child = Node(m.name,start=m.start)
			child.setAttributes(parseAttributes(html[m.start:html.find('>',m.start)]))
			child.parent = current_node
			current_node.addChild(child)
			current_node = child

			if m.name in singletons:
				if current_node.parent is not None:
					current_node = current_node.parent	

		if m.type == 'close':
			if text:
				child = Node('text',start=text_start,text=text)
				current_node.addChild(child)
			if current_node.parent is not None:
				current_node = current_node.parent
	return current_node

def main():
	parser = argparse.ArgumentParser(description = 'convert html snippets to elm functions')
	parser.add_argument('--t',type=str,help='input html')
	parser.add_argument('--i',type=str,help='input file')	
	args = parser.parse_args()
	
	if args.t == None and args.i == None:
		print('Either --t or --i must be provided')
		sys.exit(0)

	if args.t is not None:
		html = args.t
	else:
		html = open(args.i,'r').read()

	print(format_elm(parse_tree(html)))

if __name__ == '__main__':
	main()