# tests/test_tokenize.py
import re
from blocktype import tokenize_and_convert_to_html

# Define TOKEN_PATTERN
TOKEN_PATTERN = re.compile(
    r"(\*\*.+?\*\*|__.+?__|\*.+?\*|_.+?_|\`.+?\`|\~\~.+?\~\~|!\[.*?\]\(.*?\)|\[.*?\]\(.*?\))"
)

# Define tokenize function
def tokenize(markdown):
    """Split the markdown block into tokens of markdown tags and plain text."""
    tokens = []
    last_end = 0  # Keeps track of the last position in the string
    
    # Iterate over all the regex matches
    for match in TOKEN_PATTERN.finditer(markdown):
        start, end = match.span()
        
        # Add any plain text before the current token
        if last_end < start:
            tokens.append(markdown[last_end:start])
        
        # Add the matched token
        tokens.append(match.group())
        
        # Update the last_end pointer
        last_end = end
    
    # Add any plain text remaining after the last token
    if last_end < len(markdown):
        tokens.append(markdown[last_end:])
    
    return tokens







if __name__ == "__main__":
    example = "Disney _didn't ruin it_. **I like Tolkien**. See [this link](https://example.com)."
    html_output = tokenize_and_convert_to_html(example)
    print(f"Markdown: {example}")
    print(f"HTML: {html_output}")


    