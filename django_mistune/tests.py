import os
import re

from unittest import TestCase

from .utils import markdown, markdown_pdfcommand

'''
How to run:
python -m unittest django_mistune.tests
'''

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
    def setUp(self):
        import django; django.setup()

    def test_markdown_extensions(self):
        folder, names = listdir('testdata')
        for key in names:
            # yield render, folder, key
            html, result = render(folder, key)
            self.assertEqual(html, result, key)


class PdfTest(TestCase):
    def setUp(self):
        import django; django.setup()

    def test_emphasis(self):
        text = '_italics_'
        rules = [('paragraph','<em>italics</em>')]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_double_emphasis(self):
        text = '**bold**'
        rules = [('paragraph','<strong>bold</strong>')]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_strikethrough(self):
        text = '~~strike~~'
        rules = [('paragraph','<del>strike</del>')]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_misc_formatting(self):
        text = '_italics_, **bold**, ~~strike~~'
        rules = [('paragraph','<em>italics</em>, <strong>bold</strong>, <del>strike</del>')]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_links(self):
        text = 'http://auto.link <auto@email> [link](http://link)'
        rules = [('paragraph','<a href="http://auto.link">http://auto.link</a> <a href="mailto:auto@email">auto@email</a> <a href="http://link">link</a>')]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_header_1(self):
        text = '#### Just Magnetism'
        rules = [('header_4', 'Just Magnetism')]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_header_2(self):
        text = '#### Magnetism _and_ more...'
        rules = [('header_4', 'Magnetism <em>and</em> more...')]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_table(self):
        text = '''
col1 | col2
---|:---:
**1** | 2 | ~~3~~
'''
        rules = [('table', [[('col1', {'header': True, 'align': None}), ('col2', {'header': True, 'align': 'center'})], [('<strong>1</strong>', {'header': False, 'align': None}), ('2', {'header': False, 'align': 'center'}), ('<del>3</del>', {'header': False, 'align': None})]])]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)




