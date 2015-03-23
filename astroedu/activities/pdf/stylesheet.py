from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

from . import colors

def initStyleSheet(stylesheet):

    stylesheet.add(ParagraphStyle(name='Normal',
        fontName = 'Normal',
        textColor = colors.TEXT_COLOR,
        fontSize = 11,
        leading = 14,
        spaceBefore = 11,
        spaceAfter = 11,
        #   leftIndent = 12,
        allowWidows = 0,
        allowOrphans = 0,
        alignment = TA_JUSTIFY,
        ))

    stylesheet.add(ParagraphStyle(name='Disclaimer', parent=stylesheet['Normal'],
        fontName = 'Normal-Italic',
        fontSize = 7,
        leading = 8,
        spaceBefore = 7,
        ))

    ###############
    ## COVER PAGE
    ###############

    stylesheet.add(ParagraphStyle(name='Title',
        fontName = 'Normal-Bold',
        textColor = colors.TEXT_COLOR,
        fontSize = 33,
        leading = 46,
        spaceAfter = 40,
        ))

    stylesheet.add(ParagraphStyle(name='Subtitle',
        fontName = 'Normal-Bold',
        textColor = colors.HEADER_COLOR,
        fontSize = 18,
        leading = 21,
        # spaceBefore = 36,
        spaceAfter = 18,
        ))

    stylesheet.add(ParagraphStyle(name='Author',
        fontName = 'Normal',
        textColor = colors.TEXT_COLOR,
        fontSize = 14,
        leading = 21,
        #   spaceBefore = 36,
        #   spaceAfter = 18,
        ))

    ###############
    ## HEADINGS
    ###############

    stylesheet.add(ParagraphStyle(name='Heading1',
        fontName = 'Normal-Bold',
        textColor = colors.HEADER_COLOR,
        fontSize = 18,
        leading = 21,
        spaceBefore = 36,
        spaceAfter = 36,
        ))

    stylesheet.add(ParagraphStyle(name='Heading2', parent=stylesheet['Heading1'],
        fontName = 'Normal',
        ))

    stylesheet.add(ParagraphStyle(name='Heading3', parent=stylesheet['Heading1'],
        fontName = 'Normal',
        fontSize = 16,
        leading = 18,
        spaceBefore = 22,
        spaceAfter = 22,
        ))

    stylesheet.add(ParagraphStyle(name='Heading4', parent=stylesheet['Heading1'],
        fontName = 'Normal-Bold',
        textColor = colors.TEXT_COLOR,
        fontSize = 11,
        leading = 13,
        spaceBefore = 11,
        spaceAfter = 11,
        ))

    stylesheet.add(ParagraphStyle(name='footer-right', parent=stylesheet['Normal'],
        alignment = TA_RIGHT,
        ))

    ###############
    ## LISTS
    ###############

    stylesheet.add(ParagraphStyle(name='List1', parent=stylesheet['Normal'],
        spaceBefore = 0,
        spaceAfter = 0,
        leftIndent = 10,
        ))

    stylesheet.add(ParagraphStyle(name='List2', parent=stylesheet['List1'],
        leftIndent = 30,
        bulletIndent = 20,
        ))

    stylesheet.add(ParagraphStyle(name='List3', parent=stylesheet['List1'],
        leftIndent = 50,
        bulletIndent = 40,
        ))

    stylesheet.add(ParagraphStyle(name='List4', parent=stylesheet['List1'],
        leftIndent = 70,
        bulletIndent = 60,
        ))


    ###############
    ## TABLES
    ###############

    stylesheet.add(ParagraphStyle(name='TableCell',
        fontName = 'Normal',
        textColor = colors.TEXT_COLOR,
        fontSize = 7,
        leading = 9,
        ))

    stylesheet.add(ParagraphStyle(name='TableHeader', parent=stylesheet['TableCell'],
        fontName = 'Normal-Bold',
        alignment = TA_CENTER,
        ))

    stylesheet.add(ParagraphStyle(name='TableCell-left', parent=stylesheet['TableCell'],
        alignment = TA_LEFT,
        ))

    stylesheet.add(ParagraphStyle(name='TableCell-center', parent=stylesheet['TableCell'],
        alignment = TA_CENTER,
        ))

    stylesheet.add(ParagraphStyle(name='TableCell-right', parent=stylesheet['TableCell'],
        alignment = TA_RIGHT,
        ))


    stylesheet.add(ParagraphStyle(name='MetaTableCell', parent=stylesheet['TableCell'],
        leading = 12,
        spaceAfter = 2,
        ))
