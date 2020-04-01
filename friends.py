import os
import urllib.request


def getHtml(url):
    html = urllib.request.urlopen(url).read()
    return html


def saveHtml(dir, file_name, file_content):
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(dir + '/' + file_name.replace('/', '_') + ".html", "wb") as f:
        f.write(file_content)


def main():
    for i in range(1, 11):
        for j in range(1, 26):
            url1 = "http://friends.tktv.net/Episodes%s/%s.html" % (str(i), str(j))
            url2 = "http://friends.tktv.net/Episodes%s/summaries/%s.html" % (str(i), str(j))
            try:
                html = getHtml(url1)
                if 'Full transcript' in str(html):
                    html = getHtml(url2)
                saveHtml("Season %s" % str(i), "Episode %s" % str(j), html)
                print("Season %s, Episode %s download successfully." % (str(i), str(j)))
            except urllib.error.HTTPError as e:
                print(e.code)


if __name__ == '__main__':
    main()

