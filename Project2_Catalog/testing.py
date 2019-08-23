# testing = []
# sample = [1, 2, 3, 4, 5]
# for i in range(len(sample)):
#     testing.append(i)

# for k in range(len(sample)):
#     print(testing[k])

# import urllib
# from io import StringIO

# URL = "https://upload.wikimedia.org/wikipedia/en/b/b4/Snowpiercer_poster.jpg"
# file = cStringIO.StringIO(urllib.urlopen(URL).read())
# img = Image.open(file)
# img.save('static/img')

# import urllib.request
# content = urllib.request.urlopen(
#     "https://en.wikipedia.org/wiki/Stranger_Things#/media/File:Stranger_Things_logo.png")
# str = ""
# for line in content:
#     str += line
# with open("yourfile", "r") as f:
#     content = f.read()
#     return render_template("template.html", content=content)

for i in range(5):
    print(i)