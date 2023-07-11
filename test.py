from urllib.parse import urlparse

link = 'https://bit.ly/43ZXXko'

parse = urlparse(link)
print(parse.netloc + parse.path)