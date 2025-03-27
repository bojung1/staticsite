
class HTMLNode():
	def __init__ (self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError ("Not Implemented")

	def props_to_html(self):
		outstr = ""
		for key in self.props.keys():
			outstr += f" {key}=\"props[key]\"" 
		return outstr 

	def __repr__(self):
		outrepr = f"{self.tag}, {self.value}, {self.children}, {self.props}"
		return outrepr

	def __eq__ (self, other):
		return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props


