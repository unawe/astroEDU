# -*- coding: utf-8 -*-

from contrib.PyRTF import *
import rtfunicode

from django_mistune.utils import markdown_rtfcommand

def render(obj, filename):
    doc = Document()
    ss = doc.StyleSheet
    section = Section()
    doc.Sections.append(section)

    p = Paragraph(ss.ParagraphStyles.Heading1, obj.title.encode('rtfunicode'))
    section.append(p)

    p = Paragraph(ss.ParagraphStyles.Normal, obj.teaser.encode('rtfunicode'))
    section.append(p)

    p = Paragraph(ss.ParagraphStyles.Normal, B('Author(s): '), obj.author_list().encode('rtfunicode'))
    section.append(p)

    section.append('')

    from astroedu.activities.models import ACTIVITY_SECTIONS, ACTIVITY_METADATA
    for section_code, section_title in ACTIVITY_SECTIONS:
        commands = markdown_rtfcommand(getattr(obj, section_code))
        if commands:
            p = Paragraph(ss.ParagraphStyles.Heading2, section_title.encode('rtfunicode'))
            section.append(p)

            for name, content in commands:
                if name == 'image':
                    pass
                elif name.startswith('list_item_1'):
                    p = Paragraph(ss.ParagraphStyles.List1, u'\u2022 '.encode('rtfunicode'), content.encode('rtfunicode'))
                    section.append(p)
                elif name.startswith('list_item_2'):
                    p = Paragraph(ss.ParagraphStyles.List2, u'\u2022 '.encode('rtfunicode'), content.encode('rtfunicode'))
                    section.append(p)
                elif name.startswith('list_item_3'):
                    p = Paragraph(ss.ParagraphStyles.List3, u'\u2022 '.encode('rtfunicode'), content.encode('rtfunicode'))
                    section.append(p)
                elif name.startswith('list_item_4'):
                    p = Paragraph(ss.ParagraphStyles.List4, u'\u2022 '.encode('rtfunicode'), content.encode('rtfunicode'))
                    section.append(p)
                elif name.startswith('header_1'):
                    p = Paragraph(ss.ParagraphStyles.Heading1, content.encode('rtfunicode'))
                    section.append(p)
                elif name.startswith('header_2'):
                    p = Paragraph(ss.ParagraphStyles.Heading2, content.encode('rtfunicode'))
                    section.append(p)
                elif name.startswith('header_3'):
                    p = Paragraph(ss.ParagraphStyles.Heading3, content.encode('rtfunicode'))
                    section.append(p)
                elif name.startswith('header_4'):
                    p = Paragraph(ss.ParagraphStyles.Heading4, content.encode('rtfunicode'))
                    section.append(p)
                elif name == 'paragraph':
                    p = Paragraph(ss.ParagraphStyles.Normal, content.encode('rtfunicode'))
                    section.append(p)
                elif name == 'table':
                    spans = [TabPS.DEFAULT_WIDTH * 3] * len(content[0])
                    table = Table(*spans)
                    result = []
                    for i, row in enumerate(content):
                        for j, cell in enumerate(row):
                            fmt = cell[1]
                            if fmt['header']:
                                style = ss.ParagraphStyles.TableHeader
                            elif fmt['align']:
                                if fmt['align'] == 'left':
                                    style = ss.ParagraphStyles.TableCellLeft
                                elif fmt['align'] == 'center':
                                    style = ss.ParagraphStyles.TableCellCenter
                                elif fmt['align'] == 'right':
                                    style = ss.ParagraphStyles.TableCellRight
                            else:
                                style = ss.ParagraphStyles.TableCell
                            content[i][j] = Cell(Paragraph(style, cell[0].encode('rtfunicode')))
                        if len(content[i]) != len(content[0]):
                            content[i] = content[i][:len(content[0])]
                        table.AddRow(*content[i])
                    section.append(table)
                    p = Paragraph(ss.ParagraphStyles.Normal, '')
                    section.append(p)

                else:
                    print name
            # body = self.append_richtext(data)


    DR = Renderer()
    DR.Write(doc, file(filename, 'w'))
    print filename    


# def render(commands):
#     for command in commands:
        
