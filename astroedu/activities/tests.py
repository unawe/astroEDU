from django.test import TestCase
from django.conf import settings

from .models import bleach_clean
import markdown_utils

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

class HtmlRebaseTest(TestCase):
	def test_rebase(self):
		"""
		Tests the change in path of images needed for epub
		"""
		img_tpl = '<img src="%sactivities/attach/xxx/image.jpg"/>'
		text = img_tpl % settings.MEDIA_URL
		expected = img_tpl % (settings.MEDIA_ROOT + '/')
		self.assertEqual(expected, markdown_utils.media_rebase(text))


# def media_rebase(text):
#     # re-base media location
#     for m in re.finditer(r'src="/media/(.*?)"', text):
#         imgsrc = os.path.join(settings.MEDIA_ROOT, urllib.unquote(m.group(1)))
#         text = re.sub(r'src="/media/%s"' % m.group(1), r'src="%s"' % imgsrc, text)
