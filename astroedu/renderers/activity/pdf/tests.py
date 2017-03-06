# -*- coding: utf-8 -*-
import os
import re

from unittest import TestCase

from .renderer import markdown_pdfcommand

'''
How to run:
python -m unittest activities.pdf.tests
'''

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

    def test_lists(self):
        text = '''
- 1
  - 2
  - 3
- 4
  - 5
'''
        rules = [('list_item_1', '1'), ('list_item_2', '2'), ('list_item_2', '3'), ('list_item_1', '4'), ('list_item_2', '5'), ]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_lists_spaced(self):
        text = '''
- 1

- 4
'''
        rules = [('list_item_1', '1'), ('list_item_1', '4'), ]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

    def test_lists_spaced_2(self):
        text = '''

- 1

    - 2
    - 3
'''
        rules = [('list_item_1', '1'), ('list_item_2', '2'), ('list_item_2', '3'), ]
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

#     def test_table_emptycell(self):
#         text = '''
#  | col2
# ---|---
# A | B
# '''
#         rules = [('table', [[(' ', {'header': True, 'align': None}), ('col2', {'header': True, 'align': None})], [('A', {'header': False, 'align': None}), ('B', {'header': False, 'align': None})]])]
#         result = markdown_pdfcommand(text)
#         self.assertEqual(rules, result)

    def test_table_emptycell_nbsp_utf(self):
        text = '''
 | col2
---|---
A | B
'''
        rules = [('table', [[(' ', {'header': True, 'align': None}), ('col2', {'header': True, 'align': None})], [('A', {'header': False, 'align': None}), ('B', {'header': False, 'align': None})]])]
        result = markdown_pdfcommand(text)
        self.assertEqual(rules, result)

#     def test_table_emptycell_nbsp_utf_weirdbug(self):
#         text = '''
# - 1
#   - 2
#
#  | col2
# ---|---
# A | B
# '''
#         rules = [('list_item_1', '1'), ('list_item_2', '2'), ('table', [[(' ', {'header': True, 'align': None}), ('col2', {'header': True, 'align': None})], [('A', {'header': False, 'align': None}), ('B', {'header': False, 'align': None})]])]
#         result = markdown_pdfcommand(text)
#         self.assertEqual(rules, result)


#     def test_table_emptycell_nbsp_entity(self):
#         text = '''
# &nbsp;| col2
# ---|---
# A | B
# '''
#         rules = [('table', [[(' ', {'header': True, 'align': None}), ('col2', {'header': True, 'align': None})], [('A', {'header': False, 'align': None}), ('B', {'header': False, 'align': None})]])]
#         result = markdown_pdfcommand(text)
#         self.assertEqual(rules, result)





