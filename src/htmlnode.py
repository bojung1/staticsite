
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




class LeafNode(HTMLNode):
	def __init__ (self, tag, value, props=None):
		super().__init__(tag=tag, value=value, props=props, children = [])


	def to_html(self):
		if self.value is None:
			raise ValueError ("LeafNodes must have a value and this doesn't")
		if self.tag is None:
			return str(self.value)
		
		outhtml = f"<{self.tag}"

		if self.props:
			for key, value in self.props.items():
				outhtml += f' {key}="{value}"'

		outhtml += f">{self.value}</{self.tag}>"

		return outhtml


class ParentNode(HTMLNode):
	def __init__ (self, tag, children, props=None):
		super().__init__ (tag=tag, children=children, props=props)

	def to_html(self):
		if self.tag is None:
			raise ValueError ("ParentNodes must have a tag and this doesn't")
		if self.children is None:
			raise ValueError (f"Children of ParentNodes must have a value, and this doesn't")

		outnode = f"<{self.tag}"
		

		if self.props is not None:
			for prop_name,prop_value in self.props.items():
				outnode += f' {prop_name}="{prop_value}"'

		outnode += ">"

		for child in self.children:
				outnode += child.to_html()


		outnode += f"</{self.tag}>"

		return outnode 