from __future__ import absolute_import
import re
import os.path
import urllib
import subprocess

from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from celery import shared_task

from contrib.thumbnizer import processimage
from contrib.epub import epub
from astroedu.activities import utils
from astroedu.activities.pdf import renderer as pdfrenderer
from astroedu.activities.rtf import renderer as rtfrenderer

@shared_task()
def make_thumbnail(obj):
    if obj.main_visual:
        filename = obj.main_visual.file.name
        # print os.path.basename(filename)
        # print os.path.dirname(filename)
        folder = os.path.join(settings.MEDIA_ROOT, obj.media_key())
        processimage(filename, obj.code, folder, obj.media_key())

@shared_task()
def zip_attachments(obj):
    result = 0
    zipoptions = '-jX'
    outfile = obj.download_path('zip')
    subprocess.call(['rm', '-f', outfile])
    for f in obj.attachment_list():
        result += subprocess.call(['zip', zipoptions, outfile, f.file.path])    
    return result

@shared_task()
def make_epub(obj):
    EPUB_ASSETS_ROOT = os.path.join(settings.BASE_DIR, 'share', 'epub-assets')
    template = get_template('activities/epub.html')
    doc = epub.Document(obj.download_path('epub'))
    html = template.render(Context({'object': obj, }))
    # html = markdown_utils.markdown_clean(html)

    cover = os.path.join(settings.MEDIA_ROOT, obj.media_key(), 'epubcover', obj.code + '.jpg')
    if not os.path.isfile(cover):
        cover = os.path.join(EPUB_ASSETS_ROOT, 'default_cover.jpg')
    doc.files = [('images/cover.jpg', cover, None), ]

    for m in re.finditer(r'''<img[^>]*src=['"]([^"']*)['"][^>]*>''', html):
        full, local = utils.local_resource(m.group(1))
        doc.files.append((local, full, None))

    html = html.replace(settings.MEDIA_URL, '')
    doc.files.append(('%s.xhtml' % obj.code, None, html))

    doc.metadata = {
        'title': obj.title + ' - astroEDU Activity',
        'author': obj.author.name,
        'description': obj.teaser,
        'book_id': 'http://astroedu.iau.org%s' % obj.get_absolute_url(),
        'book_id_type': 'URI',
        'language': 'en',
    }

    doc.compile()

@shared_task()
def make_pdf(obj):
    pdfrenderer.Renderer().generate_one(obj, obj.download_path('pdf'))

@shared_task()
def make_rtf(obj):
    rtfrenderer.render(obj, obj.download_path('rtf'))

