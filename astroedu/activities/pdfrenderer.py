import os.path
import re

from django.conf import settings
from astroedu.activities import markdown_utils

from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import cm

from reportlab.platypus import BaseDocTemplate, Frame, Image, Paragraph, NextPageTemplate, PageBreak, PageTemplate, FrameBreak
from reportlab.lib.styles import ParagraphStyle

from contrib.pdf.pdfrenderer import PdfRendererBase, AweImage
# from astroedu.activities.models import Activity

DESTFOLDER = os.path.join(settings.MEDIA_ROOT, 'activities/download')
ASSETS_ROOT = os.path.join(settings.PROJECT_DIR, 'share', 'pdf-assets')
DEBUG = False

IMAGE_MAX_WIDTH = 13.2*cm
# PPI = 150
# IMAGE_SCALE = 72./PPI


# In the cover:
# Title: 33pt
# Normal text: 18pt and line height 21pt

# Inside:
# Titles: 18pt
# Normal text: 11pt and line height 14pt

def test():
    from astroedu.activities.models import Activity
    from astroedu.activities import tasks
    tasks.make_pdf(Activity.objects.get(slug='1301'))
# from astroedu.activities.pdfrenderer import test; test()


#### FLOWABLES ####

class SectionHeader(Paragraph):
    def __init__(self, renderer, text, style, icon):
        Paragraph.__init__(self, text, style)
        self.renderer = renderer
        self.icon = icon

    def draw(self):
        canvas = self.canv
        Paragraph.draw(self)
        self.renderer.paint_image(self.icon, -3.5*cm, -0.7*cm, canvas, mask='auto', scale=0.8)

#### END FLOWABLES ####



class Renderer(PdfRendererBase):
    lang = 'en'
    data = {}

    def __init__(self):
        PdfRendererBase.__init__(self, assets_root=ASSETS_ROOT)
        # self.register_font('Title1', 'fonts/Gotham-Bold.ttf')
        self.register_font('Normal', normal='fonts/Gotham-Book.ttf', bold='fonts/Gotham-Bold.ttf', italic='fonts/Gotham-BookItalic.ttf', boldItalic='fonts/Gotham-BoldItalic.ttf')

    def footer(self, canvas, doc):
        canvas.saveState()
        p = Paragraph('<b>iau.org/<font color="#F78606">astroedu</font></b>', self.styles['footer-right'])
        w, h = p.wrap(doc.width, doc.bottomMargin)
        p.drawOn(canvas, doc.leftMargin, 1.4*cm)
        canvas.restoreState()


    def onPageStartOne(self, canvas, doc):
        self.paint_image(os.path.join(ASSETS_ROOT, 'astroEDU_pdf_cover.png'), 'left', 'top', canvas, mask='auto', scale='fill_width')

    def onPageEndOne(self, canvas, doc):
        self.footer(canvas, doc)
        #self.paint_image(os.path.join(ASSETS_ROOT, 'background_page1.png'), 0, 0, canvas, mask='auto')

    def onPageStartNormal(self, canvas, doc):
        pass

    def onPageEndNormal(self, canvas, doc):
        self.footer(canvas, doc)
        canvas.saveState()
        canvas.setLineWidth(.02*cm)
        canvas.setStrokeColorRGB(*self.normalizeRGB('#F78606'))
        canvas.line(5.5*cm, 28.2*cm, 5.5*cm, 30*cm)
        canvas.setStrokeColorRGB(*self.normalizeRGB('#B0B0AE'))
        canvas.line(5.5*cm, 2.2*cm, self.page_width, 2.2*cm)
        canvas.restoreState()
        self.paint_image(os.path.join(ASSETS_ROOT, 'astroedu_logo.png'), 5.5*cm, 1.1*cm, canvas, mask='auto', scale=0.6)

    def process(self, obj):
        result = {}
        result['title'] = obj.title
        result['teaser'] = obj.teaser
        result['author'] = obj.author.name + ', ' + obj.institution.name
        result['description'] = process_paragraph_list(obj.description)
        result['materials'] = process_paragraph_list(obj.materials)
        result['goals'] = process_paragraph_list(obj.goals)
        result['objectives'] = process_paragraph_list(obj.objectives)
        result['background'] = process_paragraph_list(obj.background)
        result['fulldesc'] = process_paragraph_list(obj.fulldesc)
        result['evaluation'] = process_paragraph_list(obj.evaluation)
        result['curriculum'] = process_paragraph_list(obj.curriculum)
        result['additional_information'] = process_paragraph_list(obj.additional_information)
        result['conclusion'] = process_paragraph_list(obj.conclusion)
        self.data.update(result)

    def render(self, obj, file):
        style = ParagraphStyle(name='Title')
        # style = self.styles['Title']
        style.fontName = 'Normal-Bold'

        style.textColor = '#676867'
        style.fontSize = 33
        style.spaceAfter = 40
        style.leading = 46
        self.add_style(style)

        style = ParagraphStyle(name='Subtitle')
        style.fontName = 'Normal-Bold'
        style.textColor = '#F78606'
        style.fontSize = 18
        style.leading = 21
        # style.spaceBefore = 36
        style.spaceAfter = 18
        self.add_style(style)

        style = ParagraphStyle(name='Author')
        style.fontName = 'Normal'
        style.textColor = '#676867'
        style.fontSize = 14
        style.leading = 21
        # style.spaceBefore = 36
        # style.spaceAfter = 18
        self.add_style(style)

        style = ParagraphStyle(name='Heading1')
        # style = self.styles['Heading1']
        style.fontName = 'Normal-Bold'
        style.textColor = '#F78606'
        style.fontSize = 18
        style.spaceBefore = 36
        style.spaceAfter = 36
        self.add_style(style)

        style = ParagraphStyle(name='Heading3')
        # style = self.styles['Heading1']
        style.fontName = 'Normal'
        style.textColor = '#F78606'
        style.fontSize = 16
        style.spaceBefore = 36
        style.spaceAfter = 36
        self.add_style(style)

        style = ParagraphStyle(name='Heading4')
        # style = self.styles['Heading1']
        style.fontName = 'Normal-Bold'
        style.textColor = '#676867'
        style.fontSize = 11
        style.spaceBefore = 11
        style.spaceAfter = 11
        self.add_style(style)

        style = ParagraphStyle(name='Normal')
        # style = self.styles['Normal']
        style.fontName = 'Normal'
        style.textColor = '#676867'
        style.fontSize = 11
        style.leading = 14
        style.spaceBefore = 11
        style.spaceAfter = 11
        # style.leftIndent = 12
        style.alignment = TA_JUSTIFY
        self.add_style(style)

        style = ParagraphStyle(name='List1')
        style.fontName = 'Normal'
        style.textColor = '#676867'
        style.fontSize = 11
        style.leading = 14
        style.leftIndent = 10
        self.add_style(style)

        style = ParagraphStyle(name='List2')
        style.fontName = 'Normal'
        style.textColor = '#676867'
        style.fontSize = 11
        style.leading = 14
        style.leftIndent = 30
        style.bulletIndent = 20
        self.add_style(style)

        style = ParagraphStyle(name='footer-right')
        style.fontName = 'Normal'
        style.textColor = '#676867'
        style.fontSize = 11
        style.alignment = TA_RIGHT
        self.add_style(style)

        doc = BaseDocTemplate(file,
            showBoundary=DEBUG,
            pagesize=self.pagesize,
            title=obj.title,
            author='astroEDU',
            subject='Astronomy Education Activities',
        )

        self.process(obj)

        doc.addPageTemplates([
            PageTemplate(id='PageOne',
                frames=[
                    # Frame(2.5*cm, self.page_height - 6.5*cm, 11.5*cm, 5*cm, id='PageOneTitle'),
                    Frame(2.5*cm, 2.0*cm, self.page_width - 2*2.5*cm, 12.0*cm),
                ], onPage=self.onPageStartOne, onPageEnd=self.onPageEndOne),
            PageTemplate(id='PageNormal',
                #frames = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height),
                frames = Frame(5.5*cm, 3.5*cm, self.page_width - 8*cm, 23.7*cm),
                onPage=self.onPageStartNormal, onPageEnd=self.onPageEndNormal),
            ])

        styles = self.styles
        elements = []

        elements.append(Paragraph(self.data['title'], styles['Title']))
        elements.append(Paragraph(self.data['teaser'], styles['Subtitle']))
        elements.append(Paragraph(self.data['author'], styles['Author']))

        elements.append(NextPageTemplate('PageNormal'))
        elements.append(FrameBreak())

        if self.data['description']:
            elements.append(SectionHeader(self, 'Brief Description', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/description.png')))
            append_richtext(self, elements, self.data['description'])

        if self.data['goals']:
            elements.append(SectionHeader(self, 'Goals', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/goals.png')))
            append_richtext(self, elements, self.data['goals'])

        if self.data['objectives']:
            elements.append(SectionHeader(self, 'Learning Objectives', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/objectives.png')))
            append_richtext(self, elements, self.data['objectives'])

        if self.data['materials']:
            elements.append(SectionHeader(self, 'Materials', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/materials.png')))
            append_richtext(self, elements, self.data['materials'])

        if self.data['background']:
            elements.append(SectionHeader(self, 'Background Information', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/background.png')))
            append_richtext(self, elements, self.data['background'])

        if self.data['fulldesc']:
            elements.append(SectionHeader(self, 'Full Activity Description', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/fulldesc.png')))
            append_richtext(self, elements, self.data['fulldesc'])

        if self.data['evaluation']:
            elements.append(SectionHeader(self, 'Evaluation', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/evaluation.png')))
            append_richtext(self, elements, self.data['evaluation'])

        if self.data['curriculum']:
            elements.append(SectionHeader(self, 'Curriculum', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/curriculum.png')))
            append_richtext(self, elements, self.data['curriculum'])

        if self.data['additional_information']:
            elements.append(SectionHeader(self, 'Additional Information', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/additional_information.png')))
            append_richtext(self, elements, self.data['additional_information'])

        if self.data['conclusion']:
            elements.append(SectionHeader(self, 'Conclusion', styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/conclusion.png')))
            append_richtext(self, elements, self.data['conclusion'])

        doc.build(elements)


def append_richtext(rederer, elements, data):
    for it in data:
        if it[0] == 'img':
            elements.append(AweImage(rederer, it[1], maxwidth=IMAGE_MAX_WIDTH))
        elif it[0] == 'li1':
            elements.append(Paragraph(it[1], rederer.styles['List1'], bulletText=u'\u2022'))
        elif it[0] == 'li2':
            elements.append(Paragraph(it[1], rederer.styles['List2'], bulletText=u'\u2022'))
        elif it[0] == 'h3':
            elements.append(Paragraph(it[1], rederer.styles['Heading3']))
        elif it[0] == 'h4':
            elements.append(Paragraph(it[1], rederer.styles['Heading4']))
        else:
            elements.append(Paragraph(it[1], rederer.styles['Normal']))

# def markdown_clean(html):
#     # html = re.sub(r'</?a.*?>', '', html)
#     # html = re.sub(r' class=".*?"', '', html)
#     html = re.sub(r' alt=".*?"', '', html)
#     html = re.sub(r' title=".*?"', '', html)
#     html = re.sub(r' target=".*?"', '', html)
#     # html = re.sub(r'<span style="text-decoration: underline;">(.*)</span>', r'<u>\1</u>', html)
#     for m in re.finditer(r'src="/media/(.*?)"', html):
#         imgsrc = os.path.join(settings.MEDIA_ROOT, urllib.unquote(m.group(1)))
#         html = re.sub(r'src="/media/%s"' % m.group(1), r'src="%s"' % imgsrc, html)
#     # html = html.replace('"/media/', settings.MEDIA_ROOT + '/')
#     return html

def process_paragraph_list(text):
    return markdown_utils.markdown_tokenize(text)
# def process_paragraph_list(text):
#     html = markdown_clean(markdown.markdown(text))
#     result = []
#     list_level = 0
#     list_level_next = 0

#     while html:
#         mm = first_match([
#             ['img', re.search(r'<p><img.*? src="(.*?)".*?/></p>', html)], 
#             ['p', re.search('<p[^>]*>(.*?)</p>', html)], 
#             ['li', re.search('<li[^>]*>(.*?)</li>', html)],
#             ['li+', re.search('<li[^>]*>(.*?)<ul>', html)],
#             ['h3', re.search('<h3[^>]*>(.*?)</h3>', html)],
#             ['h4', re.search('<h4[^>]*>(.*?)</h4>', html)],
#             ['ul', re.search('<ul>', html)],
#             ['/ul', re.search('</ul>', html)],
#         ])
#         if mm:
#             print mm[0], mm[1].group(0)
#             if mm[0] == 'ul':
#                 list_level += 1
#             elif mm[0] == '/ul':
#                 list_level -= 1
#             else:
#                 if mm[0] == 'li+':
#                     list_level_next = 1
#                     mm[0] = 'li'
#                 if mm[0] == 'li':
#                     mm[0] = mm[0] + str(list_level)
#                 result.append((mm[0], mm[1].group(1)))
#                 list_level += list_level_next
#                 list_level_next = 0
#             start = mm[1].end()
#         # if img or p or li:
#         #     # item = p if p.start < li.start else li
#         #     if img and p:
#         #         print img.start(), p.start(), img.group(1) #, li.start()
#         #     if p:
#         #         print p.start()
#         #     if img and (not p or img.start() <= p.start()): # and (not li or img.start() < li.start()):
#         #         result.append(('img', img.group(1)))
#         #         start = img.end()
#         #     elif p and (not li or p.start() < li.start()):
#         #         result.append(('p', p.group(1)))
#         #         start = p.end()
#         #     elif li:
#         #         result.append(('li', li.group(1)))
#         #         start = li.end()
#         #     else:
#         #         result.append(('li', li.group(1)))
#         #         start = li.end()
#         #     print 'new start: ',  start
#             html = html[start:]
#         else:
#             html = ''
#     return result

# def local_resource(uri):
#     """
#     Returns the full file path and a relative path for the resource
#     """
#     if uri.startswith(settings.MEDIA_URL):
#         local = uri.replace(settings.MEDIA_URL, '')
#         path = os.path.join(settings.MEDIA_ROOT, local)
#     elif uri.startswith(settings.STATIC_URL):
#         local = uri.replace(settings.STATIC_URL, '')
#         path = os.path.join(settings.STATIC_ROOT, local)
#     else:
#         raise UnsupportedMediaPathException('media urls must start with %s or %s' % (settings.MEDIA_ROOT, settings.STATIC_ROOT))

#     # return path
#     return urllib.unquote(path), urllib.unquote(local)


if __name__ == '__main__':
    test()
