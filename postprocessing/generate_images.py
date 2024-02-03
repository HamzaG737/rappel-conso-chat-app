import re

from IPython.display import display, Markdown, Image


def display_text_with_images(text):
    # Modify the regex to remove potential '[voir image]' and parentheses around the URL
    image_urls = re.findall(
        r"\[.*(?:mage|lien).*\]\((https?://[^\s]+image[^\s]*)\)", text
    )

    # Replace the markdown image syntax with just the URL for splitting
    text_for_splitting = re.sub(
        r"\[.*(mage|lien).*\]\((https?://[^\s]+image[^\s]*)\)", r"\2", text
    )
    # Split text at image URLs
    parts = re.split(r"https?://[^\s]+image[^\s]*\b", text_for_splitting)
    for i in range(len(parts)):
        # Display the text part
        display(Markdown(parts[i].replace("\n", "\n\n")))

        # Display the image if it exists
        if i < len(image_urls):
            display(Image(url=image_urls[i]))
