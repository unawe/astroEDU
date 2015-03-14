import os.path

from PIL import Image as PIL

from reportlab.lib.pagesizes import A4
# from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import cm

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import BaseDocTemplate, Frame, Image, Paragraph, NextPageTemplate, PageBreak, PageTemplate, FrameBreak
from reportlab.platypus.flowables import Flowable
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.styles import StyleSheet1 # , ParagraphStyle
# from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class Styles(StyleSheet1):
    lang = 'en'
    font_overrides = {}
    
    def add(self, style):
        if self.lang in self.font_overrides:
            style.fontName = self.font_overrides[self.lang]
        if self.lang in ['ja', 'zh', 'ko']:
            style.wordWrap = 'CJK'
        StyleSheet1.add(self, style)  # StyleSheet1 is an old-style class, can't use super()

def normalizeRGB(text):
    'transforms a #RRGGBB value into a tuple usable by setFillColorRGB() and setStrokeColorRGB()'
    if text.startswith('#'):
        text = text[1:]
    return(int(text[0:2], 16)/256., int(text[2:4], 16)/256., int(text[4:6], 16)/256.)


class PdfRendererBase(object):
    def __init__(self, pagesize=A4, ppi=150, assets_root=''):
        self.pagesize = pagesize
        self.page_width = self.pagesize[0]
        self.page_height = self.pagesize[1]
        self.ppi = ppi
        self.image_scale = 72./self.ppi
        self.assets_root = assets_root
        self.styles = Styles()

    def onPageStartOne(self, canvas, doc):
        pass

    def onPageEndOne(self, canvas, doc):
        pass

    def onPageStartNormal(self, canvas, doc):
        pass

    def onPageEndNormal(self, canvas, doc):
        pass

    # def safe_font(self, name, lang):
    #     if lang in ['vi', 'ro', 'ru']:
    #         return 'DejaVuSansCondensed'
    #     elif lang == 'ar':
    #         return 'DejaVuSans'
    #     elif lang == 'ja':
    #         return 'Kochi Gothic'  # sans serif
    #         # return 'Kochi Mincho'  # serif
    #     elif lang in ['zh', 'si']:
    #         return 'HanaMinA'
    #     else:
    #         return name

    def get_dependent_image(self, name):
        #return 'images_' + str(PPI) + '/' + name
        return name

    def paint_background(self, image, canvas):
        image = self.get_dependent_image(image)
        canvas.drawImage(image, 0, 0, self.page_width, self.page_height)

    def paint_image(self, image, x, y, canvas, **kwargs):
        scale = kwargs.pop('scale', 1)
        surfaceHeight = kwargs.pop('surfaceHeight', self.page_height)
        # origin = kwargs.pop('origin', BOTTOM_LEFT_ORIGIN)

        # print image
        image = self.get_dependent_image(image)
        im = PIL.open(image)
        w, h = im.size
        if scale == 'fill_width':
            scale = 1.0 * self.page_width / (self.image_scale * w)

        w *= self.image_scale * scale
        h *= self.image_scale * scale
        if x == 'left':
            x = 0
        elif x == 'right':
            x = self.page_width-w
        elif x == 'center':
            x = (self.page_width-w)/2
        if y == 'top':
            y = surfaceHeight-h
        elif y == 'bottom':
            y = 0
        elif y == 'center':
            y = (surfaceHeight-h)/2
        canvas.drawImage(image, x, y, w, h, **kwargs)
        # print x, y, w, h
        return (x, y, w, h)

    def draw_constrained_text(self, text, style, canvas, x, y, w, h, border=False):
        fontSize = style.fontSize
        from reportlab.pdfbase.pdfmetrics import stringWidth
        from reportlab.lib.utils import simpleSplit

        # while stringWidth(text, style.fontName, fontSize) > w:
        #   fontSize -= 1

        # while len(simpleSplit(text, style.fontName, fontSize, w)) > num_lines:
        #   fontSize -= 1
        if style.wordWrap == 'CJK':
            while stringWidth(text, style.fontName, fontSize) > w:
                fontSize -= 1
            height = fontSize
            lines = [text]
        else:
            height = h + 1
            while height > h:
                # print stringWidth(text, style.fontName, fontSize), w
                lines = simpleSplit(text, style.fontName, fontSize, w)
                height = fontSize * len(lines)
                # print height, h
                fontSize -= 1
            fontSize += 1

        # print 'H: ', h, height
        y_offset = (h - height)/2
        if border:
            canvas.rect(x, y, w, h, stroke=1, fill=0)  # outer border
            canvas.rect(x, y+y_offset, w, height, stroke=1, fill=0)

        lines.reverse()
        for line in lines:
            textobject = canvas.beginText()
            textobject.setTextOrigin(x, y+y_offset)
            textobject.setFont(style.fontName, fontSize)
            # print style.textColor, str(style.textColor)
            textobject.setFillColorRGB(*normalizeRGB(style.textColor))
            #textobject.setCharSpace(1.5)
            textobject.textLine(line)
            canvas.drawText(textobject)
            y_offset += fontSize

    def render(self, obj, file):
        raise NotYetImplemented()

    def generate_one(self, obj, path):
        # path = os.path.join(self.destfolder, '%s.%s' % (obj.id, self.file_ext))
        # if not self.overwrite and os.path.exists(path):
        #     return
        f = open(path, 'w')
        self.render(obj, f)
        f.close()

    def register_font(self, name, normal=None, bold=None, italic=None, boldItalic=None, langs=[]):

        # register languages overrides
        if langs:
            for lang in langs:
                self.font_overrides[lang] = name

        # regsiter font family with reportlab
        if normal is None and bold is None and italic is None and boldItalic is None:
            raise ValueError('No font file was specified')
        if normal:
            pdfmetrics.registerFont(TTFont(name, os.path.join(self.assets_root, normal)))
            normal = name
        if bold:
            pdfmetrics.registerFont(TTFont(name + '-Bold', os.path.join(self.assets_root, bold)))
            bold = name + '-Bold'
        if italic:
            pdfmetrics.registerFont(TTFont(name + '-Italic', os.path.join(self.assets_root, italic)))
            italic = name + '-Italic'
        if boldItalic:
            pdfmetrics.registerFont(TTFont(name + '-BoldItalic', os.path.join(self.assets_root, boldItalic)))
            boldItalic = name + '-BoldItalic'
        pdfmetrics.registerFontFamily(name, normal=normal, bold=bold, italic=italic, boldItalic=boldItalic)


class AweImage(Image):
    '''PPI-aware image (knows its proper size)'''
    
    def __init__(self, renderer, pathname, maxwidth=None, **kwargs):
        Image.__init__(self, pathname, **kwargs)
        self.renderer = renderer
        self.maxwidth = maxwidth
        self.scale = self.renderer.image_scale

    def wrap(self, availWidth, availHeight):
        w, h = Image.wrap(self, availWidth, availHeight)
        if self.maxwidth:
            if w * self.scale > self.maxwidth:
                self.scale *= self.maxwidth / (w * self.scale)
        w *= self.scale
        h *= self.scale
        # print '... ', w, h
        return w, h

    def draw(self):
        canvas = self.canv
        canvas.scale(self.scale, self.scale)
        Image.draw(self)


class AweImages(Flowable):
    def __init__(self, renderer, images):
        self.renderer = renderer
        self.images = images

    def getSpaceBefore(self):
        return 0*cm

    def getSpaceAfter(self):
        return 0*cm

    def wrap(self, availWidth, availHeight):
        return (availWidth, 54)

    def split(self, availWidth, availHeight):
        return []

    def draw(self):
        canvas = self.canv
        x = 0
        y = 0.12*cm
        (x, _y, w, _h) = self.renderer.paint_image(os.path.join(self.renderer.assets_root, 'footer-left.png'), x, 0, canvas, mask='auto')
        for image in self.images:
            x += w + 0.1*cm
            (x, _y, w, _h) = self.renderer.paint_image(image, x, y, canvas, scale=self.renderer.image_scale, mask='auto')
        x += w + 0.1*cm
        (x, _y, w, _h) = self.renderer.paint_image(os.path.join(self.renderer.assets_root, 'footer-right.png'), x, 0, canvas, mask='auto')











