import string


def generate_filename(info):
    """generate a filename based on the convention"""
    template = string.Template("$t.jpg")
    filename = template.substitute(info)
    return filename

