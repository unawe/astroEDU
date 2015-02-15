from contrib.pitufo import *
from django_mistune.utils import markdown_rtfcommand

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
                    image_full_path, image_local_path = utils.local_resource(urllib.unquote(content))
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
        
