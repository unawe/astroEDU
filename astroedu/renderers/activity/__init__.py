import os
import re
import subprocess

from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from sorl.thumbnail import get_thumbnail
from contrib.epub.epub import Document as EpubDocument

from activities import utils
from .pdf import renderer as pdfrenderer
from .rtf import renderer as rtfrenderer


def pdf(obj, path, site_url=None):
    pdfrenderer.Renderer().generate_one(obj, path)


def rtf(obj, path, site_url=None):
    rtfrenderer.render(obj, path)


def zip(obj, path, site_url=None):
    result = 0
    zipoptions = '-jX'
    subprocess.call(['rm', '-f', path])
    for f in obj.attachment_list():
        if f.file:
            # skip missing files
            result += subprocess.call(['zip', zipoptions, path, f.file.path])

    for f in obj.attachment_list():
        if f.file:
            # skip missing files
            result += subprocess.call(['zip', zipoptions, path, f.file.path])

    for f in obj.languageattachment_list():
        if f.file:
            # skip missing files
            result += subprocess.call(['zip', zipoptions, path, f.file.path])

    return result


def epub(obj, path, site_url=None):
    from activities.models import ACTIVITY_SECTIONS
    EPUB_ASSETS_ROOT = os.path.join(settings.BASE_DIR, 'share', 'epub-assets')
    template = get_template('activities/activity_epub.html')
    doc = EpubDocument(path)
    html = template.render(Context({'object': obj, 'sections': ACTIVITY_SECTIONS, }))
    # html = markdown_utils.markdown_clean(html)

    if obj.main_visual:
        im = get_thumbnail(obj.main_visual, settings.THUMBNAIL_ALIASES['epubcover'], crop='center')
        cover = os.path.join(settings.MEDIA_ROOT, im.name)
    else:
        cover = os.path.join(EPUB_ASSETS_ROOT, 'default_cover.jpg')
    doc.files = [('images/cover.jpg', cover, None), ]

    for m in re.finditer(r'''<img[^>]*src=['"]([^"']*)['"][^>]*>''', html):
        full, local = utils.local_resource(obj.attachment_url(m.group(1)))
        doc.files.append((local, full, None))

    html = html.replace(settings.MEDIA_URL, '')
    doc.files.append(('%s.xhtml' % obj.code, None, html))

    doc.metadata = {
        'title': obj.title + ' - astroEDU Activity',
        'author': obj.author_list(),
        'description': obj.teaser,
        'book_id': settings.SITE_URL + obj.get_absolute_url(),
        'book_id_type': 'URI',
        'language': 'en',
    }

    doc.compile()
