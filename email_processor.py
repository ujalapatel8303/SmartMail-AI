import re


def clean_email(text):
    """
    Cleans unnecessary blank lines and spaces
    from the email.
    """

    text = re.sub(r'\n+', '\n', text)

    text = text.strip()

    return text