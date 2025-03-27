from textnode import TextNode, TextType


print ("hello world")


def main():
	derp = TextNode("derp", TextType.LINK, "https://www.boot.dev")
	print (derp)


if __name__ == "__main__":
    main()