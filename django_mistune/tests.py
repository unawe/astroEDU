import os
import re

from django.test import TestCase

from . import markdown

root = os.path.dirname(__file__)


def render(folder, name):
    filepath = os.path.join(folder, name + '.text')
    with open(filepath) as f:
        content = f.read()

    html = markdown(content)

    filepath = os.path.join(folder, name + '.html')
    with open(filepath) as f:
        result = f.read()

    html = re.sub(r'\s', '', html)
    result = re.sub(r'\s', '', result)

    return html, result

def listdir(folder):
    folder = os.path.join(root, folder)
    files = os.listdir(folder)
    # files = filter(lambda o: o.endswith('.text'), files)
    # names = map(lambda o: o[:-5], files)
    names = [o[:-5] for o in files if o.endswith('.text')]
    return folder, names


class MarkdownTest(TestCase):
    longMessage = True
    def test_markdown_extensions(self):
        folder, names = listdir('testdata')
        for key in names:
            # yield render, folder, key
            html, result = render(folder, key)
            self.assertEqual(html, result, key)
