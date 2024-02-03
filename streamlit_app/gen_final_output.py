import re
import string
import streamlit as st


def display_text_with_images(text):
    """
    Display text with associated images.

    Args:
        text (str): The text to be displayed.

    Returns:
        None
    """

    # Modify the regex to remove potential '[voir image]' and parentheses around the URL
    image_urls = re.findall(
        r"https?://[^\s]+image[^\s]*.jpg",
        text,
        flags=re.IGNORECASE,
    )

    # Replace the markdown image syntax with just the URL for splitting
    text_for_splitting = re.sub(
        r"-? +?!?\[lien vers l'image\]\s*\(?(https?://[^\s]+image[^\s]*.jpg)\)?",
        r"\1 \n ",
        text,
        flags=re.IGNORECASE,
    )

    # Split text at image URLs
    parts = re.split(r"https?://[^\s]+image[^\s]*.jpg", text_for_splitting)

    for i, part in enumerate(parts):
        # If there is punctuation character, parts[i] must have at least one alpha character.
        if any(char in string.punctuation for char in part) and not any(
            char.isalpha() for char in part
        ):
            continue
        # Display the text part
        st.markdown(part.replace("\n", "\n\n"))

        # Display the image if it exists
        if i < len(image_urls):
            st.image(image_urls[i])
