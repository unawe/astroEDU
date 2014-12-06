import re
import os
import markdown
import urllib

# from bs4 import BeautifulSoup

from django.conf import settings

ALLOWED_TAGS = ('p', 'ul', 'h3', 'h4')

def markdown_clean(text):
    # remove annoying attributes
    text = re.sub(r' alt=".*?"', '', text)
    text = re.sub(r' title=".*?"', '', text)
    text = re.sub(r' target=".*?"', '', text)

    # remove line breaks
    # text = re.sub(r'\n', ' ', text)
    # text = re.sub(r'\s*<br\s*\/?>\s*', ' ', text)
    text = re.sub(r'\<br\s*\/?>', ' ', text)

    # make sure images are isolated
    text = re.sub(r'(!\[.*?\]\(.*?\))', r'\n\1\n', text)

    # disable markdown ordered lists
    text = re.sub(r'ol>', 'ul>', text)

    # TEMPORARY: fix second-level lists
    text = re.sub(r'--', '   -', text)

    return text

def media_rebase(text):
    # re-base media location
    for m in re.finditer(r'src="/media/(.*?)"', text):
        imgsrc = os.path.join(settings.MEDIA_ROOT, urllib.unquote(m.group(1)))
        text = re.sub(r'src="/media/%s"' % m.group(1), r'src="%s"' % imgsrc, text)

    return text

def first_match(matches):
    start = 999999999  # infinity
    result = None
    for mm in matches:
        if mm[1] and mm[1].start() < start:
            start = mm[1].start()
            result = mm
    return result

def markdown_tokenize(text):
    result = []

    html = markdown_clean(markdown.markdown(text))
    html = media_rebase(html)
    soup = BeautifulSoup(html)

    for child in soup.children:
        tag = child.name
        if tag:
            if tag not in ALLOWED_TAGS:
                print 'TAG NOT ALLOWED: %s' % tag 
            else:
                if tag in ('p', 'h3', 'h4'):
                    child2 = child.findChild()
                    if child2 and child2.name == 'img':
                        result.append(('img', child2['src']))
                    else:
                        result.append((tag, child.renderContents()))
                elif tag == 'ul':
                    markdown_tokenize_list(child, result)

    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(result)

    return result

def markdown_tokenize_list(node, result, level=1):
    for child in node.children:
        tag = child.name
        if tag:
            if tag == 'li':
                result.append(('li%d' % level, child.renderContents()))
                print 'li', child
            elif tag == 'ul':
                print child
            else:
                print tag


def markdown_tokenize_0(text):
    html = markdown_clean(markdown.markdown(text))
    result = []
    list_level = 0
    list_level_next = 0

    while html:
        mm = first_match([
            ['img', re.search(r'<p><img.*? src="(.*?)".*?/></p>', html)], 
            ['p', re.search('<p[^>]*>(.*?)</p>', html)], 
            ['li', re.search('<li[^>]*>(.*?)</li>', html)],
            ['li+', re.search('<li[^>]*>(.*?)<ul>', html)],
            ['h3', re.search('<h3[^>]*>(.*?)</h3>', html)],
            ['h4', re.search('<h4[^>]*>(.*?)</h4>', html)],
            ['ul', re.search('<ul>', html)],
            ['/ul', re.search('</ul>', html)],
        ])
        if mm:
            # print mm[0], mm[1].group(0)
            remainder = html[:mm[1].start()].strip()
            if remainder:
                print 'WARNING: unprocessed text: ', remainder

            if mm[0] == 'ul':
                list_level += 1
            elif mm[0] == '/ul':
                list_level -= 1
            else:
                if mm[0] == 'li+':
                    list_level_next = 1
                    mm[0] = 'li'
                if mm[0] == 'li':
                    mm[0] = mm[0] + str(list_level)
                result.append((mm[0], mm[1].group(1)))
                list_level += list_level_next
                list_level_next = 0
            start = mm[1].end()
            html = html[start:]
        else:
            html = ''
    return result
