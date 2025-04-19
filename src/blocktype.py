import re
from enum import Enum
from stringparse import markdown_to_blocks, text_node_to_html_node
from htmlnode import HTMLNode
from textnode import TextType, TextNode


### this is here just to make regex matching in a case statement not a fucking nightmare. 
class RegexEqual(str):
	def __eq__(self, pattern):
		return bool(re.search(pattern, self))

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"



#single block of markdown text is imput 
#the lesson sucks in explaining this
#but this is a single block, so an item of a list, which is a string
#coopted some clever regex to make this work, I think it's insane python doesn't natively do this

def block_to_block_type(md_block):
	# Strip leading/trailing whitespace from the entire block
	stripped_block = md_block.strip()

	if not stripped_block:
		return BlockType.PARAGRAPH

	# Check for fenced code blocks (```...```)
	if stripped_block.startswith('```') and stripped_block.endswith('```'):
		# This covers both multi-line and single-line code blocks
		return BlockType.CODE
	
	# If we get here, check other block types
	match RegexEqual(md_block):
		case r"^#{1,6}[ ].*":
			return BlockType.HEADING
		case r"^>":
			return BlockType.QUOTE
		case r"^\s*[*-] ":  # Match either * or - with potential leading whitespace
			return BlockType.UNORDERED_LIST
		case r"^[1-9][0-9]*[.]":
			return BlockType.ORDERED_LIST
		case _:
			# Check for indented code blocks (4 spaces or 1 tab)
			lines = md_block.split('\n')
			if all(line.startswith('	') or line.startswith('\t') or not line.strip() for line in lines):
				return BlockType.CODE
			
			return BlockType.PARAGRAPH




#markdown is a full markdown document which probably means a string here
# probably. vague ass instructions
# m2block is going to be a list of strings
# block is going then be raw string blocks with markup in them

TOKEN_PATTERN = re.compile(r'(\*\*|_|`|~{2})')  # Matches bold (**), italic (_), code (`), strikethrough (~~)

def markdown_to_html_node(markdown):
	parent_node = HTMLNode("div", None, {}, [])

	m2blocks = markdown_to_blocks(markdown)
	for block in m2blocks:
		btype = block_to_block_type(block)
		match (btype):
			case BlockType.HEADING:
				hxtag = which_heading(block)
				headingblock = block.lstrip("# ")
				parsed_child_nodes = text_to_children(headingblock)
				outputnode = HTMLNode(hxtag, None , {}, parsed_child_nodes)
				parent_node.children.append(outputnode)
			
			case BlockType.CODE:
				# Extract code content by removing the first and last lines (the triple backticks)
				lines = block.split('\n')
				
				# If we have at least 3 lines (opening backticks, content, closing backticks)
				if len(lines) >= 3:
					# Join everything except first and last lines
					code_content = '\n'.join(lines[1:-1]) + '\n'
				else:
					# Handle the case of empty code block or malformed block
					code_content = ""
				
				# Create a code node directly instead of relying on text_node_to_html_node
				code_node = HTMLNode("code", code_content, {}, [])
				pre_node = HTMLNode("pre", None, {}, [code_node])
				parent_node.children.append(pre_node)


			case BlockType.QUOTE:
				# Split the block into lines, strip the '>' from each line, and rejoin
				quoteblock = block.strip()
				lines = quoteblock.split('\n')
				# Remove '>' from the beginning of each line and any leading/trailing spaces
				cleaned_lines = [line.lstrip('>').strip() for line in lines]
				# Join the lines back together with spaces
				cleaned_content = ' '.join(cleaned_lines)
				parsed_child_nodes = text_to_children(cleaned_content)
				outputnode = HTMLNode("blockquote", None, {}, parsed_child_nodes)
				parent_node.children.append(outputnode)

			case BlockType.UNORDERED_LIST:
				list_items = block.splitlines()
				cleaned_items = [re.sub(r'^\s*[*-]\s+', '', item) for item in list_items]
				list_item_nodes = [] 

				for item in cleaned_items:
					children = text_to_children(item)
					list_item_node = HTMLNode("li", None, {}, children)
					list_item_nodes.append(list_item_node)

				outputnode = HTMLNode("ul", None, {}, list_item_nodes)
				parent_node.children.append(outputnode)

			case BlockType.ORDERED_LIST:
				list_items = block.splitlines()
				cleaned_items = [re.sub(r'^\d+\.\s+', '', item) for item in list_items]				

				list_item_nodes = [] 
				for item in cleaned_items:
					children = text_to_children(item)
					list_item_node = HTMLNode("li", None, {}, children)
					list_item_nodes.append(list_item_node)
				
				outputnode = HTMLNode("ol", None, {}, list_item_nodes)
				parent_node.children.append(outputnode)

			case BlockType.PARAGRAPH:
				block_text = ' '.join(block.split('\n'))
				parsed_child_nodes = text_to_children(block_text)
				outputnode = HTMLNode("p", None, {}, parsed_child_nodes)
				parent_node.children.append(outputnode)


	return parent_node





def tokenize(markdown):
			"""Split the markdown block into tokens of markdown tags and plain text."""
			return [token for token in TOKEN_PATTERN.split(markdown) if token]

def parse_inline_markdown(markdown):
	"""
	Parse a block of inline markdown and convert it into a tree-like structure.
	Handles nested tags using a stack.
	
	Args:
		markdown (str): The markdown string to parse.
		
	Returns:
		dict: A tree-like structure representing the parsed markdown.
	"""
	tokens = tokenize(markdown)  # Split the markdown input into tokens
	stack = []  # Stack to track opened markdown tags
	root = {"tag": None, "content": []}  # The top-level node
	current_node = root  # Start at the top-level node
	
	for token in tokens:
		if token in {"**", "_", "`", "~~"}:
			# Check if this is a closing tag for the current open tag
			if stack and stack[-1]["tag"] == token:
				# This is a closing tag - pop from stack
				stack.pop()
				# Move back to the parent node
				current_node = stack[-1] if stack else root
			else:
				# This is an opening tag - create new node
				new_node = {"tag": token, "content": []}
				current_node["content"].append(new_node)
				stack.append(new_node)
				current_node = new_node
		else:
			# Plain text - add to current node's content
			current_node["content"].append({"tag": None, "text": token})
	
	# Handle any unclosed tags by popping them and moving back to root
	while stack:
		stack.pop()
	
	return root


def text_to_children(markdown):
	"""
	Converts a block of inline markdown into a list of HTMLNode objects.

	Args:
		markdown (str): The inline Markdown string.

	Returns:
		list: A list of HTMLNode objects.
	"""
	# Step 1: Parse the inline markdown into a tree structure
	tree = parse_inline_markdown(markdown)
			
	# Step 2: Recursively convert the tree-structure to list of HTMLNodes
	def convert_tree_to_nodes(node):
			# Base case: If plain text
		if node["tag"] is None:
			text_node = TextNode(node.get("text", ""), TextType.TEXT)
			return text_node_to_html_node(text_node)
			
		# Otherwise, create an HTMLNode for the tag and process its children
		children = [convert_tree_to_nodes(child) for child in node["content"]]
		html_tag = {
			"**": "b",  # Bold text
			"_": "i",   # Italic text
			"`": "code",  # Inline code
			"~~": "del"  # Strikethrough
		}.get(node["tag"], None)  # Map markdown tags to HTML tags
		return HTMLNode(html_tag, None, {}, children)
			
	# Step 3: Process the root content into nodes
	return [convert_tree_to_nodes(child) for child in tree["content"]]


def parse_markdown(markdown):
			"""Parse markdown with nested tags using a stack."""
			tokens = tokenize(markdown)
			stack = []  # This will track currently open tags
			root = {"tag": "div", "content": []}  # The top-level parent node
			current_node = root  # Start with the root node

			for token in tokens:
				if token in {"**", "_", "`", "~~"}:  # Opening tag
				# Push a new node for the tag onto the stack
					new_node = {"tag": token, "content": []}
					stack.append(new_node)
					# Attach it to the current node's content
					current_node["content"].append(new_node)
					current_node = new_node  # Dive into the new node

				elif token in {"**", "_", "`", "~~"} and stack and stack[-1]["tag"] == token:  # Closing tag
					# Pop the top node from the stack as it's now closed
					stack.pop()
					# Move back up to the parent node
					current_node = stack[-1] if stack else root

				else:  # Plain text
					# Add plain text to the current node's content
					current_node["content"].append({"tag": None, "text": token})

			return root



# if it's a BlockType.HEADING call this so you can figure out whether it should be h1 through h6 
# this assumes that the previous stuff already checked to make sure it's a valid heading

def which_heading(blockstring):
	# Count the number of # at the beginning of the string
	count = 0
	for char in blockstring:
		if char == '#':
			count += 1
		else:
			break
	
	# Ensure there's a space after the # characters and count is between 1-6
	if count >= 1 and count <= 6 and blockstring[count:count+1] == " ":
		return f"h{count}"
	else:
		raise Exception("Invalid heading format")









