
class HTMLNode():
	def __init__ (self, tag=None, value=None, props=None, children=None):
		self.tag = tag
		self.value = value
		self.props = props or {}
		self.children = children or []


	def to_html(self):
		# Base case: Text-only node
		if self.tag is None:
			return self.value or ""
		
		# Serialize attributes
		attr_string = " ".join(f'{key}="{value}"' for key, value in self.props.items())
		if attr_string:
			attr_string = " " + attr_string
		
		# Handle self-closing tags like <img>
		if self.tag in ["img", "br", "hr"]:  # Add other self-closing tags if needed
			return f"<{self.tag}{attr_string} />"
		
		# Handle <a> tags for links
		if self.tag == "a":
			print("Processing link:", self)
			child_html = "".join(child.to_html() for child in self.children)  # For nested children
			return f"<{self.tag}{attr_string}>{child_html or self.value}</{self.tag}>"
		
		# Default case: Handle tags with children and value
		child_html = "".join(child.to_html() for child in self.children)
		return f"<{self.tag}{attr_string}>{self.value or ''}{child_html}</{self.tag}>"


	def props_to_html(self):
		outstr = ""
		for key in self.props.keys():
			outstr += f' {key}="{self.props[key]}"'
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
		if children is None:
			raise ValueError ("Children of ParentNodes must have a value, and this doesn't")
		super().__init__ (tag=tag, children=children, props=props)

	def to_html(self):
		if self.tag is None:
			raise ValueError ("ParentNodes must have a tag and this doesn't")
		if self.children is None:
			raise ValueError ("Children of ParentNodes must have a value, and this doesn't")

		outnode = f"<{self.tag}"
		

		if self.props is not None:
			for prop_name,prop_value in self.props.items():
				outnode += f' {prop_name}="{prop_value}"'

		outnode += ">"

		for child in self.children:
				outnode += child.to_html()


		outnode += f"</{self.tag}>"

		return outnode 