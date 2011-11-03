MAX_LENGTH = 256

def shorten(content):
    content_str = str(content)
    return content_str if len(content_str) < MAX_LENGTH else "%s..." % content_str[0:MAX_LENGTH-3]

