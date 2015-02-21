from contrib.pitufo import *
from django_mistune import markdown
from django_mistune.utils import Flattener, TreeRenderer


ACTIVITY_METADATA_COLS = 3


class RtfFlattener(Flattener):

    def inline(self, text=None):
        return [] if text is None else [text]

    def double_emphasis(self, content):
        result = []
        result.append('\\b ')
        result += content
        result.append('\\b0 ')
        return result
            
    def emphasis(self, content):
        result = []
        result.append('\\i ')
        result += content
        result.append('\\i0 ')
        return result

    def strikethrough(self, content):
        result = []
        result.append('\\strike ')
        result += content
        result.append('\\strike0 ')
        return result
            
    def link(self, link, content):
        result = []
        result.append('{\\field{\\*\\fldinst HYPERLINK "%s"}{\\fldrslt ' % str(link))
        result += content
        result.append('}}')
        return result


def markdown_rtfcommand(text, inline=None, block=None):
    tree = markdown(text, TreeRenderer(), inline, block)
    result = RtfFlattener().parse(tree)
    return result


def render(obj, filename):
    doc = Document()

    doc.meta['title'] = obj.title
    doc.meta['subject'] = obj.theme
    doc.meta['author'] = obj.author_list()
    # doc.meta['company'] = u'astroEDU'
    doc.meta['keywords'] = obj.keywords
    doc.meta['doccomm'] = obj.teaser
    # doc.meta['copyright'] = 

    doc.append(Paragraph([obj.title], style='Heading 1'))
    doc.append(Paragraph([obj.teaser]))
    doc.append(Paragraph([obj.author_list()]))
    doc.append(Paragraph([]))


    from astroedu.activities.models import ACTIVITY_SECTIONS, ACTIVITY_METADATA

    table = Table()
    for i, (code, title, value) in enumerate(obj.metadata_aslist()):
        if i % ACTIVITY_METADATA_COLS == 0:
            table_row = TableRow()
            table.append(table_row)
        table_row.append(TableCell(['\\b ', title, '\\b0\line\n', value], style='Table Cell'))
    doc.append(table)

    for section_code, section_title in ACTIVITY_SECTIONS:
        commands = markdown_rtfcommand(getattr(obj, section_code))
        if commands:
            doc.append(Paragraph([section_title], style='Heading 2'))

            for name, content in commands:
                if name == 'paragraph':
                    doc.append(Paragraph(content))
                elif name.startswith('header_'):
                    level = int(name[len('header_'):])
                    doc.append(Heading(content, level=level))
                elif name.startswith('list_item_'):
                    level = int(name[len('list_item_'):])
                    doc.append(BulletedListItem(content, level=level))
                elif name == 'image':
                    from astroedu.activities import utils
                    import urllib
                    image_full_path, image_local_path = utils.local_resource(urllib.unquote(obj.attachment_url(content)))
                    doc.append(Image(image_full_path))
                elif name == 'table':
                    table = Table()
                    for i, row in enumerate(content):
                        table_row = TableRow()
                        for j, cell in enumerate(row):
                            fmt = cell[1]
                            if fmt['header']:
                                style = 'Table Header'
                            else:
                                style = 'Table Cell'
                                if fmt['align']:
                                    # this can be one of left, right, center
                                    style += ' ' + fmt['align'].capitalize()
                            table_row.append(TableCell(cell[0], style=style))
                        table.append(table_row)
                    doc.append(table)
                else:
                    print name


    with open(filename, 'w') as f:
        doc.write(f)
        
