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

#TOKEN_PATTERN = re.compile(r'(\*\*|_|`|~{2})')  # Matches bold (**), italic (_), code (`), strikethrough (~~)



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


			case BlockType.IMAGE:
				match = re.match(r'!\[([^\]]+)\]\(([^\)]+)\)', block)  # Regex for ![alt](src)
				if match:
					alt_text = match.group(1)
					src = match.group(2)
					img_node = HTMLNode("img", None, {"src": src, "alt": alt_text}, [])
					parent_node.children.append(img_node)


			case BlockType.LINK:
				match = re.match(r'\[([^\]]+)\]\(([^\)]+)\)', block)  # Regex for [text](href)
				if match:
					link_text = match.group(1)
					href = match.group(2)
					text_node = HTMLNode("#text", link_text, {}, [])
					a_node = HTMLNode("a", None, {"href": href}, [text_node])
					parent_node.children.append(a_node)


	return parent_node


def is_indented(line):
    # Check if a line is indented (has spaces or tabs at the beginning)
    return line.startswith('  ') or line.startswith('\t')

def get_indentation_level(line):
    # Count leading spaces to determine indentation level
    # We might say 2 spaces = 1 level
    spaces = len(line) - len(line.lstrip(' '))
    return spaces // 2  # Or whatever indentation scheme you use


TOKEN_PATTERN = re.compile(
	r'(\*\*.+?\*\*|_.+?_|\`.+?\`|~~.+?~~|!\[[^\]]*\]\([^)]+\)|\[[^\]]*\]\([^)]+\))'
)


def tokenize(markdown):
	"""Split the markdown block into tokens of markdown tags and plain text."""
	tokens = []
	last_end = 0  # Keeps track of the last position in the string

	for match in TOKEN_PATTERN.finditer(markdown):
		start, end = match.span()

		# Add plain text (if any) before this token
		if last_end < start:
			tokens.append(markdown[last_end:start])

		# Add the matched token
		tokens.append(match.group())

		# Update position of last match
		last_end = end

	# Add any plain text remaining after the last token
	if last_end < len(markdown):
		tokens.append(markdown[last_end:])

	return tokens


def convert_token_to_html(token):
	"""Convert individual Markdown tokens to their HTML representation."""
	# Bold `**text**` or `__text__`
	if token.startswith("**") and token.endswith("**"):
		return f"<b>{token[2:-2]}</b>"

	# Italic `_text_` or `*text*`
	elif (token.startswith("_") and token.endswith("_")) or (token.startswith("*") and token.endswith("*")):
		return f"<i>{token[1:-1]}</i>"

	# Inline code `` `code` ``
	elif token.startswith("`") and token.endswith("`"):
		return f"<code>{token[1:-1]}</code>"

	# Strikethrough `~~text~~`
	elif token.startswith("~~") and token.endswith("~~"):
		return f"<del>{token[2:-2]}</del>"

	# Link `[text](url)`
	elif token.startswith("[") and token.endswith(")"):
		try:
			text, url = token[1:].split("](", 1)
			url = url[:-1]  # Remove the closing `)`
			return f'<a href="{url}">{text}</a>'
		except ValueError:
			return token  # Return raw token if it doesn't match format

	# Image `![alt](url)`
	elif token.startswith("![") and token.endswith(")"):
		try:
			alt, url = token[2:].split("](", 1)
			url = url[:-1]  # Remove the closing `)`
			return f'<img src="{url}" alt="{alt}">'
		except ValueError:
			return token  # Return raw token if it doesn't match format

	# If token doesn't match any pattern, return it as-is
	return token


def tokenize_and_convert_to_html(markdown):
	"""Tokenize markdown and convert tokens to HTML."""
	tokens = []
	last_end = 0  # Keeps track of the last position in the string

	# Iterate over all the regex matches
	for match in TOKEN_PATTERN.finditer(markdown):
		start, end = match.span()

		# Add any plain text before the current token
		if last_end < start:
			tokens.append(markdown[last_end:start])

		# Add the matched token (converted to HTML)
		tokens.append(convert_token_to_html(match.group()))

		# Update the last_end pointer
		last_end = end

	# Add any plain text remaining after the last token
	if last_end < len(markdown):
		tokens.append(markdown[last_end:])

	return "".join(tokens)  # Join tokens back into a full HTML string



def parse_inline_markdown(markdown):
	"""
	Parse a block of inline markdown and convert it into a tree-like structure.
	Handles nested tags, links, and images using a stack.
	
	Args:
		markdown (str): The markdown string to parse.
		
	Returns:
		dict: A tree-like structure representing the parsed markdown.
	"""
	tokens = tokenize(markdown)  # Split the markdown input into tokens

	print("Tokens:", tokens)

	stack = []  # Stack to track opened markdown tags
	root = {"tag": None, "content": []}  # The top-level node
	current_node = root  # Start at the top-level node

	# Regex patterns for links and images
	link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
	image_pattern = re.compile(r'!\[([^\]]+)\]\(([^)]+)\)')
	
	for token in tokens:
		# Handle links
		if link_pattern.match(token):
			match = link_pattern.match(token)
			print("Matched link:", match.groups())  # Debug link parsing
			text = match.group(1)  # Link text
			href = match.group(2)  # Link URL
			link_node = {
				"tag": "a", 
				"content": [{"tag": None, "text": text}], 
				"attributes": {"href": href}
			}
			current_node["content"].append(link_node)
		
		# Handle images
		elif image_pattern.match(token):
			match = image_pattern.match(token)
			alt = match.group(1)  # Alt text
			src = match.group(2)  # Image URL
			image_node = {
				"tag": "img", 
				"content": [], 
				"attributes": {"src": src, "alt": alt}
			}
			current_node["content"].append(image_node)

		# Handle bold, italic, inline code, and strikethrough
		elif token in {"**", "_", "`", "~~"}:
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
		
		# Handle plain text
		else:
			current_node["content"].append({"tag": None, "text": token})
	
	# Handle any unclosed tags by popping them and moving back to root
	while stack:
		stack.pop()
	
	return root


def text_to_children(markdown):
	"""
	Convert a block of inline markdown to HTML nodes.
	"""
	# Use your existing tokenization and conversion
	html_content = tokenize_and_convert_to_html(markdown)
	
	# Create a temporary parent node
	parent = HTMLNode("div", None, {}, [])
	
	# Create text nodes for the HTML content
	text_node = TextNode(html_content, TextType.TEXT)
	parent.children.append(text_node_to_html_node(text_node))
	
	# Return the children of the parent
	return parent.children





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









