import os.path
import re
import urllib
import copy

from django.conf import settings
# from activities import markdown_utils

from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, Frame, Image, Paragraph, Table, NextPageTemplate, PageBreak, PageTemplate, FrameBreak, TableStyle, KeepTogether, Spacer 
from reportlab.platypus.flowables import Flowable

from django_mistune import markdown
from django_mistune.utils import Flattener, TreeRenderer
from contrib.pdf.pdfrenderer import PdfRendererBase, AweImage, normalizeRGB

from activities import utils
from . import colors
from .stylesheet import initStyleSheet

DESTFOLDER = os.path.join(settings.MEDIA_ROOT, 'activities/download')
ASSETS_ROOT = os.path.join(settings.BASE_DIR, 'share', 'pdf-assets')
DEBUG = False

IMAGE_MAX_WIDTH = 13.2*cm
# PPI = 150
# IMAGE_SCALE = 72./PPI
ACTIVITY_METADATA_COLS = 3

# def test():
#     from activities.models import Activity
#     from activities import tasks
#     a = Activity.objects.available().get(code='0000')
#     tasks.make_pdf(a)
# # import django; django.setup(); from activities.pdf.renderer import test; test()


class PdfFlattener(Flattener):

    # def empty_inline(self):
    #     return ''

    def inline(self, text=None):
        return '' if text is None else text

    def double_emphasis(self, content):
        return '<strong>%s</strong>' % content

    def emphasis(self, content):
        return '<em>%s</em>' % content

    def strikethrough(self, content):
        return '<del>%s</del>' % content

    def link(self, link, content):
        if link != content:
            content += ' (%s)' % link
        return '<a href="%s">%s</a>' % (link, content)


def markdown_pdfcommand(text, inline=None, block=None):
    tree = markdown(text, TreeRenderer(), inline, block)
    result = PdfFlattener().parse(tree)
    return result


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


class HorizontalRuler(Flowable):

    def wrap(self, availWidth, availHeight):
        self.availWidth = availWidth
        return (availWidth, .5*cm)

    def split(self, availWidth, availHeight):
        return []

    def draw(self):
        canvas = self.canv

        canvas.saveState()
        canvas.setLineWidth(.02*cm)
        canvas.setStrokeColorRGB(*normalizeRGB(colors.HEADER_COLOR))
        canvas.line(0, 0, self.availWidth, 0)
        canvas.restoreState()


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

    def onPageStartNormal(self, canvas, doc):
        pass

    def onPageEndNormal(self, canvas, doc):
        self.footer(canvas, doc)
        canvas.saveState()
        canvas.setLineWidth(.02*cm)
        canvas.setStrokeColorRGB(*normalizeRGB(colors.HEADER_COLOR))
        canvas.line(5.5*cm, 28.2*cm, 5.5*cm, 30*cm)
        canvas.setStrokeColorRGB(*normalizeRGB(colors.FOOTER_LINE_COLOR))
        canvas.line(5.5*cm, 2.2*cm, self.page_width, 2.2*cm)
        canvas.restoreState()
        self.paint_image(os.path.join(ASSETS_ROOT, 'astroedu_logo.png'), 5.5*cm, 1.1*cm, canvas, mask='auto', scale=0.6)

    def render(self, obj, file):
        from activities.models import ACTIVITY_SECTIONS

        self.relativise_img_src = obj.attachment_url

        initStyleSheet(self.styles)

        doc = BaseDocTemplate(
            file,
            showBoundary=DEBUG,
            pagesize=self.pagesize,
            title=obj.title,
            author='astroEDU',
            subject='Astronomy Education Activities',
        )

        # self.process(obj)

        doc.addPageTemplates([
            PageTemplate(
                id='PageOne',
                frames=[
                    # Frame(2.5*cm, self.page_height - 6.5*cm, 11.5*cm, 5*cm, id='PageOneTitle'),
                    Frame(2.5*cm, 2.0*cm, self.page_width - 2*2.5*cm, 12.0*cm),
                ], onPage=self.onPageStartOne, onPageEnd=self.onPageEndOne),
            PageTemplate(
                id='PageNormal',
                # frames = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height),
                frames = Frame(5.5*cm, 3.5*cm, self.page_width - 8*cm, 23.7*cm),
                onPage=self.onPageStartNormal, onPageEnd=self.onPageEndNormal),
            ])

        styles = self.styles
        elements = []

        ## COVER PAGE
        elements.append(Paragraph(obj.title, styles['Title']))
        elements.append(Paragraph(obj.teaser, styles['Subtitle']))
        elements.append(Paragraph(obj.author_list(), styles['Author']))

        elements.append(NextPageTemplate('PageNormal'))
        elements.append(FrameBreak())

        ## SECOND PAGE
        meta_table_data = self._build_meta_table(obj)
        meta_table_style = TableStyle([
                # ('INNERGRID', (0,0), (-1,-1), 0.25, normalizeRGB(colors.TEXT_COLOR)),
                # ('BOX', (0,0), (-1,-1), .5, normalizeRGB(colors.TEXT_COLOR)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ])
        # elements.append(Spacer(.5*cm, .5*cm))
        elements.append(KeepTogether(Table(meta_table_data, style=meta_table_style)))
        elements.append(HorizontalRuler())
        elements.append(Spacer(.5*cm, .5*cm))

        for section_code, section_title in ACTIVITY_SECTIONS:
            data = markdown_pdfcommand(getattr(obj, section_code))
            if data:
                header = SectionHeader(self, section_title, styles['Heading1'], icon=os.path.join(ASSETS_ROOT, 'sections-orange/%s.png' % section_code))
                body = self._append_richtext(data)
                # elements.append(header)
                # elements += body
                elements.append(KeepTogether([header, body[0]]))
                elements += body[1:]

        data = markdown_pdfcommand(obj.get_footer_disclaimer())
        disclaimer = self._append_richtext(data, normal_style='Disclaimer')
        disclaimer.insert(0, HorizontalRuler())
        elements.append(Spacer(.5*cm, .5*cm))
        # elements += disclaimer
        elements.append(KeepTogether(disclaimer))

        doc.build(elements)

    def _append_richtext(self, data, normal_style='Normal'):
        result = []
        for name, content in data:
            if name == 'paragraph':
                result.append(Paragraph(content, self.styles[normal_style]))
            elif name.startswith('header'):
                header_level = name[len('header_'):]
                result.append(Paragraph(content, self.styles['Heading'+header_level]))
            elif name.startswith('list_item'):
                list_level = name[len('list_item_'):]
                result.append(Paragraph(content, self.styles['List'+list_level], bulletText=u'\u2022'))
            elif name == 'image':
                image_full_path, image_local_path = utils.local_resource(urllib.parse.unquote(self.relativise_img_src(content)))
                result.append(AweImage(self, image_full_path, maxwidth=IMAGE_MAX_WIDTH))
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
                        value = cell[0] if cell[0] else u'\u00A0'  # a non-breaking space makes sure an empty row has enough height
                        content[i][j] = Paragraph(value, style)
                table_style = TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, normalizeRGB(colors.TEXT_COLOR)),
                        ('BOX', (0, 0), (-1, -1), .5, normalizeRGB(colors.TEXT_COLOR)),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ])
                result.append(KeepTogether(Table(content, style=table_style)))
                result.append(Spacer(.5*cm, .5*cm))
            else:
                raise Exception('Unexpected command: ', name)
        return result

    def _build_meta_table(self, obj):
        result = []
        for i, (code, title, value) in enumerate(obj.metadata_aslist()):
            if i % ACTIVITY_METADATA_COLS == 0:
                row = []
                result.append(row)
            row.append([
                Paragraph('<b>%s</b>' % title, self.styles['MetaTableCell']),
                Paragraph(value, self.styles['MetaTableCell']),
            ])

        return result


if __name__ == '__main__':
    test()
