import os.path
import re
import urllib
import copy

from django.conf import settings
# from astroedu.activities import markdown_utils

from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, Frame, Image, Paragraph, Table, NextPageTemplate, PageBreak, PageTemplate, FrameBreak, TableStyle, KeepTogether, Spacer 

from django_mistune.utils import markdown_pdfcommand
from contrib.pdf.pdfrenderer import PdfRendererBase, AweImage

from . import colors
from .stylesheet import initStyleSheet

DESTFOLDER = os.path.join(settings.MEDIA_ROOT, 'activities/download')
ASSETS_ROOT = os.path.join(settings.BASE_DIR, 'share', 'pdf-assets')
DEBUG = False

IMAGE_MAX_WIDTH = 13.2*cm
# PPI = 150
# IMAGE_SCALE = 72./PPI


def test():
    from astroedu.activities.models import Activity
    from astroedu.activities import tasks
    a = Activity.objects.get(code='0000')
    tasks.make_pdf(a)
# import django; django.setup(); from astroedu.activities.pdf.renderer import test; test()


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
    # lang = 'en'

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
        canvas.setStrokeColorRGB(*self.normalizeRGB(colors.HEADER_COLOR))
        canvas.line(5.5*cm, 28.2*cm, 5.5*cm, 30*cm)
        canvas.setStrokeColorRGB(*self.normalizeRGB(colors.FOOTER_LINE_COLOR))
        canvas.line(5.5*cm, 2.2*cm, self.page_width, 2.2*cm)
        canvas.restoreState()
        self.paint_image(os.path.join(ASSETS_ROOT, 'astroedu_logo.png'), 5.5*cm, 1.1*cm, canvas, mask='auto', scale=0.6)

    def render(self, obj, file):

        initStyleSheet(self.styles)

        doc = BaseDocTemplate(file,
            showBoundary=DEBUG,
            pagesize=self.pagesize,
            title=obj.title,
            author='astroEDU',
            subject='Astronomy Education Activities',
        )

        # self.process(obj)

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

        elements.append(Paragraph(obj.title, styles['Title']))
        elements.append(Paragraph(obj.teaser, styles['Subtitle']))
        elements.append(Paragraph(obj.author_list(), styles['Author']))

        elements.append(NextPageTemplate('PageNormal'))
        elements.append(FrameBreak())

        from astroedu.activities.models import ACTIVITY_SECTIONS, ACTIVITY_METADATA
        for section_code, section_title in ACTIVITY_SECTIONS:
            data = markdown_pdfcommand(getattr(obj, section_code))
            if data:
                header = SectionHeader(self, section_title, styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/%s.png' % section_code))
                body = self.append_richtext(data)
                # elements.append(header)
                # elements += body
                elements.append(KeepTogether([header, body[0]]))
                elements += body[1:]

        doc.build(elements)

    def append_richtext(self, data):
        result = []
        for name, content in data:
            if name == 'image':
                image_name = content[len(settings.MEDIA_URL):]
                image_path = os.path.join(settings.MEDIA_ROOT, urllib.unquote(image_name))
                result.append(AweImage(self, image_path, maxwidth=IMAGE_MAX_WIDTH))
            elif name.startswith('list_item'):
                list_level = name[len('list_item_'):]
                result.append(Paragraph(content, self.styles['List'+list_level], bulletText=u'\u2022'))
            elif name.startswith('header'):
                header_level = name[len('header_'):]
                result.append(Paragraph(content, self.styles['Heading'+header_level]))
            elif name == 'paragraph':
                result.append(Paragraph(content, self.styles['Normal']))
            elif name == 'table':
                for i, row in enumerate(content):
                    for j, cell in enumerate(row):
                        fmt = cell[1]
                        if fmt['header']:
                            style = self.styles['TableHeader']
                        elif fmt['align']:
                            style = self.styles['TableCell-' + fmt['align']]
                        else:
                            style = self.styles['TableCell']
                        content[i][j] = Paragraph(cell[0], style)
                table_style = TableStyle([
                        ('INNERGRID', (0,0), (-1,-1), 0.25, self.normalizeRGB(colors.TEXT_COLOR)),
                        ('BOX', (0,0), (-1,-1), .5, self.normalizeRGB(colors.TEXT_COLOR)),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                    ])
                result.append(KeepTogether(Table(content, style=table_style)))
                result.append(Spacer(.5*cm, .5*cm))
            else:
                raise Exception('Unexpected command: ', name)
        return result


if __name__ == '__main__':
    test()
