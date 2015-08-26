# -*- coding: utf-8 -*-

import os
import re
import zipfile
import mimetypes
import json

if __name__ == '__main__':
    import utils
else:
    from . import utils

BUILD_TOC = True


class Document(object):

    files = []
    metadata = {}
    
    def __init__(self, file):

        #super(Document, self).__init__(file, 'w') #, zipfile.ZIP_DEFLATED)
        #zipfile.ZipFile.__init__(self, file, 'w') #, zipfile.ZIP_DEFLATED)
        self.epub = zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)
        mimetypes.init()

        # The first file must be named "mimetype"
        self.write_file('mimetype', 'application/epub+zip', zipfile.ZIP_STORED)

    def write_file(self, filename, content, encoding=None):
        if encoding:
            bytes = content.encode(encoding)
        else:
            bytes = content
        self.epub.writestr(filename, bytes)

    def compile(self):
        cover_id = None
        #merged = ''
        manifest = ''
        metadata = self.metadata
        spine = '    <itemref idref="toc" />\n' if BUILD_TOC else ''
        navmap = ''
        toc = []
        playorder = 1

        for i, file in enumerate(self.files):
            name = file[0]
            fullpath = file[1]
            content = file[2]
            ext = os.path.splitext(name)[1].lower()
            mediatype = mimetypes.types_map[ext]
            file_id = 'file_%d' % (i+1)
            
            # add file to manifest
            manifest += '    <item id="%s" href="%s" media-type="%s"/>\n' % (file_id, name, mediatype)
            
            # add file to spine and toc
            # print name, mediatype
            if mediatype in ['application/xhtml+xml', 'text/html']:
                if name.find(u'cover') != -1:
                    spine = '    <itemref idref="%s" />\n' % file_id + spine
                else:
                    spine += '    <itemref idref="%s" />\n' % file_id
                if fullpath and not content:
                    with open(fullpath) as f:
                        content = unicode(f.read(), 'utf-8')
                title, level = utils.extract_title(content)
                #merged += extract_body(content)
                if title:
                    # print name, title
                    utils.append_toc(toc, file_id, title, name, level)
                    navmap += '''    <navPoint class="chapter" id="%s" playOrder="%d">
      <navLabel><text>%s</text></navLabel>
      <content src="%s"/>
    </navPoint>
''' % (file_id, playorder, title, name)
                    playorder += 1
                # else:
                #     print name
        
            # cover?
            if mediatype.startswith('image/') and re.search('cover', name, re.IGNORECASE):
                metadata['cover'] = file_id
            # add to zip
            #self.epub.write(file, 'OEBPS/'+name)
            if mediatype in ['application/xhtml+xml', 'text/html']:
                self.write_file('OEBPS/'+name, content, 'utf-8')
            else:
                if fullpath:
                    self.epub.write(fullpath, 'OEBPS/'+name)
                else:
                    self.write_file('OEBPS/'+name, content)
    
        manifest += '''    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
        '''
        if BUILD_TOC: 
            manifest += '''    <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" />
        '''
        
        ##############################
        # META-INF/container.xml
        self.write_file('META-INF/container.xml', u'''<?xml version="1.0" encoding="UTF-8"?>
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
          </rootfiles>
        </container>''', 'utf-8')
        
        ##############################
        # OEBPS/content.opf
        index_tpl = u'''<?xml version="1.0" encoding="UTF-8"?>
        <package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">
          <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        %(metadata)s
          </metadata>
          <manifest>
        %(manifest)s
          </manifest>
          <spine toc="ncx">
        %(spine)s
          </spine>
        </package>'''
        
        # book id and related metadata
        metadata['book_id_scheme'] = ''
        if 'book_id' not in metadata:
            metadata['book_id'] = uuid.uuid4()
            metadata['book_id_type'] = 'UUID'
            metadata['book_id_scheme'] = 'urn:uuid:'
        elif metadata['book_id_type'] == 'ISBN':
            metadata['book_id_scheme'] = 'urn:isbn:'
            
        ##############################
        # metadata
        metadata_tpl = u'''    <dc:title>%(title)s</dc:title>
            <dc:identifier id="BookId" opf:scheme="%(book_id_type)s">%(book_id_scheme)s%(book_id)s</dc:identifier>
            <dc:creator opf:role="aut">%(author)s</dc:creator>
            <dc:description>%(description)s</dc:description>
            <meta name="cover" content="%(cover)s" />
        '''
        metadata_opt = {
            'language' : '    <dc:language xsi:type="dcterms:RFC3066">%(language)s</dc:language>\n',
            'dublincore' : '    <%(key)s>%(value)s</%(key)s>\n',
        }
        
        ##############################
        # OEBPS/toc.ncx
        toc_tpl = u'''<?xml version="1.0" encoding="UTF-8"?>
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
        %(toc_metadata)s
          
          <navMap>
        %(navmap)s
          </navMap>
        </ncx>'''
        toc_metadata_tpl = u'''  <head>
            <meta name="dtb:uid" content="%(book_id)s"/>
            <meta name="dtb:depth" content="1"/>
            <meta name="dtb:totalPageCount" content="0"/>
            <meta name="dtb:maxPageNumber" content="0"/>
          </head>
          
          <docTitle><text>%(title)s</text></docTitle>
          <docAuthor><text>%(author)s</text></docAuthor>
        '''
        
        # Write the index
        metadata_text = metadata_tpl % metadata
        if metadata['language']:
            metadata_text += metadata_opt['language'] % {'language': metadata['language'], }
        for (k, v) in metadata.items():
            if k.startswith('dc:') or k.startswith('dcterms:'):
                metadata_text += metadata_opt['dublincore'] % {'key': k, 'value': v, }
        
        index_text = index_tpl % {
          'metadata': metadata_text,
          'manifest': manifest,
          'spine': spine,
        }
        self.write_file('OEBPS/content.opf', index_text, 'utf-8')
        
        # Write toc.ncx
        toc_metadata_text = toc_metadata_tpl % metadata
        metadata['navmap'] = navmap
        toc_text = toc_tpl % {
          'toc_metadata': toc_metadata_text,
          'navmap': navmap,
        }
        self.write_file('OEBPS/toc.ncx', toc_text, 'utf-8')
        
        #print toc_text
        #print json.dumps(toc)
        #print toc_ncx(toc)
        
        # Write toc.xhtml
        if BUILD_TOC:
            toc_html = u'''<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <title>Table of Contents</title>
        <style type="text/css">
        ul { list-style-type: none; margin-left:1em; padding-left:0em; }
        a { text-decoration: none; color: inherit }
        li { margin-top: 0.2em; }
        li:last-child { margin-bottom: 1em; }
        </style>
        </head>
        <body>
        <h1>Table of Contents</h1>
        <div>%s</div>
        </body>
        </html>
        ''' % utils.toc_html(toc)
            self.write_file('OEBPS/toc.xhtml', toc_html, 'utf-8')


if __name__ == '__main__':
    import sys

    src_folder = '.'
    out_file = None
    if len(sys.argv) > 1:
        src_folder = sys.argv[1]
    if len(sys.argv) > 2:
        out_file = sys.argv[2]

    src_folder = os.path.abspath(src_folder)
    if not out_file:
        out_file = os.path.dirname(src_folder) + '.epub'

    print src_folder
    print out_file

    doc = Document(out_file)

    for root, dirs, files in os.walk(src_folder):
        # print root, files
        for name in files:
            if not name.startswith('.'):
                full = os.path.join(root, name)
                local = os.path.relpath(full, start=src_folder)
                doc.files.append((local, full, None))

    with open('metadata.json') as f:
        doc.metadata = json.load(f)

    doc.compile()
