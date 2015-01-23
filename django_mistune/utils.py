import mistune

from django.conf import settings

def markdown(text, renderer=None, inline=None, block=None):
    #TODO: rules = ['table', 'fenced_code', 'footnotes', 'autolink', 'strikethrough',]
    my_settings = settings.MISTUNE_STYLES if hasattr(settings, 'MISTUNE_STYLES') else {}
    md = MyMarkdown(renderer, inline, block, **my_settings)
    result = md.render(text)
    return result


class MyMarkdown(mistune.Markdown):
    # fix for uneven tables
    def output_table(self):
        aligns = self.token['align']
        cell = self.renderer.placeholder()

        # header part
        header = self.renderer.placeholder()
        for i, value in enumerate(self.token['header']):
            align = aligns[i] if i < len(aligns) else None
            flags = {'header': True, 'align': align}
            cell += self.renderer.table_cell(self.inline(value), **flags)

        header += self.renderer.table_row(cell)

        # body part
        body = self.renderer.placeholder()
        for i, row in enumerate(self.token['cells']):
            cell = self.renderer.placeholder()
            for j, value in enumerate(row):
                align = aligns[j] if j < len(aligns) else None
                flags = {'header': False, 'align': align}
                cell += self.renderer.table_cell(self.inline(value), **flags)
            body += self.renderer.table_row(cell)

        return self.renderer.table(header, body)
