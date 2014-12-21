from django.test import TestCase

from models import bleach_clean


class BleachTest(TestCase):
	def test_white_listed(self):
		"""
		Tests that white listed html tags are not removed by bleach
		"""
		texts = [
			u'Superscript: <sup>italics</sup>',
			u'Subscript: <sub>italics</sub>',
			u'Links: <a href="http://www.uanwe.org/" target="_blank">UNAWE</a>',
			u'Italics: <em>italics</em>',
			u'Paragraph: <p>italics</p>',
		]
		for text in texts:
			self.assertEqual(text, bleach_clean(text))

	def test_table(self):
		"""
		Tests that tables are correctly bleached
		"""
		text = u'Table: <table><tr><th>col</th><td>data</td></tr></table>'
		expected = u'Table: <table><tbody><tr><th>col</th><td>data</td></tr></tbody></table>'
		self.assertEqual(expected, bleach_clean(text))

	def test_line_breaks(self):
		"""
		Tests that tables are correctly bleached
		"""
		text = u'Line breaks: <br> </br> <br/> <br />'
		expected = u'Line breaks: <br/> <br/> <br/> <br/>'
		self.assertEqual(expected, bleach_clean(text))

	def test_bad_html(self):
		"""
		Tests not allowed html is bleached
		"""
		texts = [
			(u'Script: <script>nasty java script...', u'Script: &lt;script&gt;nasty java script...', )
		]
		for text, expected in texts:
			self.assertEqual(expected, bleach_clean(text))

