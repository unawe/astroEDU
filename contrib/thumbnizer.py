#!/usr/bin/python

import sys, os, stat, glob, tempfile, time, json, shutil

from django.conf import settings

# def init_dev():
#     defs = {}
#     sys.path.append('/Users/rino/Workspaces/sites/unawe/virtualenv/lib/python2.7/site-packages/')
#     defs['KEEPFILE'] = False
#     defs['REPROCESS'] = False
#     defs['LOCKFILE'] = '/Users/rino/Projects/unawe/processimages/djangoplicity_image_processing'
#     defs['DATAFILE'] = '/Users/rino/Projects/unawe/processimages/images_drop_data.json'
#     defs['SRCDIR'] = '/Users/rino/Projects/unawe/processimages/archives_drop/'
#     defs['DESTDIR'] = '/Users/rino/Workspaces/web/unawe.org/static/archives/'
#     defs['SLEEPTIME'] = 2
#     return defs


# def init_ops():
#     defs = {}
#     sys.path.append('/home/ubuntu/unawe/virtualenv/lib/python2.6/site-packages/')
#     defs['KEEPFILE'] = False
#     defs['REPROCESS'] = False
#     defs['LOCKFILE'] = '/home/mediauploader/conf/djangoplicity_image_processing'
#     defs['DATAFILE'] = '/home/mediauploader/conf/images_drop_data.json'
#     defs['SRCDIR'] = '/home/mediauploader/archives_drop/'
#     defs['DESTDIR'] = '/home/ubuntu/unawe_src/unawe.org/static/archives/'
#     defs['SLEEPTIME'] = 30
#     return defs


# def reinit_reprocess():
#     global KEEPFILE
#     KEEPFILE = True
#     global REPROCESS
#     REPROCESS = True
#     global SRCDIR
#     SRCDIR = defs['DESTDIR']
#     global SLEEPTIME
#     SLEEPTIME = 2


# if os.path.realpath(__file__).startswith('/Users/rino'):
#     defs = init_dev()
# else:
#     defs = init_ops()

from PIL import Image
# from lockfile import FileLock, AlreadyLocked

# LOCKFILE = defs['LOCKFILE']
# DATAFILE = defs['DATAFILE']
# SRCDIR = defs['SRCDIR']
# DESTDIR = defs['DESTDIR']
# SLEEPTIME = defs['SLEEPTIME']
# KEEPFILE = defs['KEEPFILE']
# REPROCESS = defs['REPROCESS']
# IMGTYPES = ['jpg', 'png', 'jpeg']
# OTHERTYPES = ['pdf', 'ppt', 'epub', 'mobi', 'ai', ]


METHOD = Image.ANTIALIAS             # best down-sizing filter (other options: NEAREST, BILINEAR, BICUBIC
CENTERING = (0.5, 0.5, )             # crop at center
# CENTERING = (0.0, 0.0, )             # crop at top-left corner
# CENTERING = (0.0, 1.0, )             # crop at top-right corner
# CENTERING = (1.0, 0.0, )             # crop at bottom-left corner
# CENTERING = (1.0, 1.0, )             # crop at bottom-right corner

# SIZES = {                            # name: (width, height, mandatory)
#     #'newsmini': (150, -100, True, ),       # fixed width, constrained height
#     'newsmini': (150, 100, True, ),       
#     'thumb': (150, -220, True, ), 
#     'thumb_android': (150, 150, True, ), 
#     'screen': (1280, 0, True, ),           # fixed width, free height
#     'potw': (240, 0, True, ),
#     'medium': (320, 0, True, ),
#     'newsfeature': (560, 230, True, ),
#     'large': (1500, 0, False, ),
#     'wallpaper1': (1024, 768, False, ),    # not mandatory: image won't be upscaled
#     'wallpaper2': (1280, 1024, False, ),
#     'wallpaper3': (1600, 1200, False, ),
#     'kidspdf': (1050, 520, True, ),
#     'epubcover': (800, 1066, True, ),
# }
# RESOURCES = {
#     'images':        {'formats': ['newsmini', 'screen', 'potw', 'medium', 'newsfeature', 'wallpaper1', 'wallpaper2', 'wallpaper3', 'kidspdf', 'thumb_android']},
#     'brochures':     {'formats': ['thumb', 'screen', 'medium', 'large', ]},
#     'education':     {'formats': ['thumb', 'screen', 'medium', 'large', ]},
#     'guides':        {'formats': ['thumb', 'screen', 'medium', 'large', ]},
#     'presentations': {'formats': ['thumb', 'screen', 'medium', 'large', ]},
#     'reports':       {'formats': ['thumb', 'screen', 'medium', 'large', ]},
#     'posters':       {'formats': ['thumb', 'screen', 'medium', 'large', ]},
#     'videos':        {'formats': ['newsmini', 'thumb', ]},
#     'books':         {'formats': ['thumb', 'screen', 'medium', 'large', ]},
#     'activities':    {'formats': ['newsmini', 'thumb', 'newsfeature', 'epubcover', ]},
# }
SIZES = settings.THUMBNIZER_SIZES
RESOURCES = settings.THUMBNIZER_KEYS


def filetype_match(name, extensions):
    result = False
    for ext in extensions:
        if os.path.splitext(name)[1][1:] == ext:
            result = True
    return result


def folder_exists_for(filename, destdir):
    filetype = os.path.splitext(filename)[1][1:]
    return os.path.exists(os.path.join(destdir, filetype))


def subset_sizes(res, mysize):
    result = {}
    # calculate original image ratio
    ratio = 1. * mysize[0] / mysize[1]

    for name in RESOURCES[res]['formats']:
        size = SIZES[name]
        # check if the size applies: it is mandatory (size[2]==True), or not larger than the original image
        if size[2] or (mysize[0] > size[0] and mysize[1] > size[1]):
            (width, height) = (size[0], size[1], )

            # calculate free height / widths
            if width <= 0 and height <= 0:
                raise Error
            elif width == 0:
                width = int(height * ratio)
            elif width < 0:
                width = min(int(height * ratio), -width)
            elif height == 0:
                height = int(width / ratio)
            elif height < 0:
                height = min(int(width / ratio), -height)
            result[name] = (width, height)
            # print name, result[name]

    return result


def presize(im, sizes):
    maxwidth = maxheight = 0
    for (width, height) in sizes.values():
        maxwidth = max(maxwidth, width)
        maxheight = max(maxheight, height)
    if maxwidth < im.size[0] and maxheight < im.size[1]:
        # ok, the input image is huge; we can do some pre-resizing
        # print im.size[0] , im.size[1]
        if float(im.size[0])/im.size[1] > float(maxwidth)/maxheight:
            size = (int(im.size[0] * float(maxheight)/im.size[1]), maxheight)
        else:
            size = (maxwidth, int(im.size[1] * float(maxwidth)/im.size[0]))
        # print 'original size: ', im.size, ', presize: ', size
        im = im.resize(size, Image.ANTIALIAS)  # this should be the fastest and lowest quality resize
        # print 'presize done'
    return im


def imagecrop(im, size, method=Image.ANTIALIAS, centering=(0.5, 0.5, )):
    if float(im.size[0])/im.size[1] > float(size[0])/size[1]:
        cropsize = (int(size[0] * float(im.size[1])/size[1]), im.size[1])
    else:
        cropsize = (im.size[0], int(size[1] * float(im.size[0])/size[0]))
    if cropsize != im.size:
        dx = im.size[0] - cropsize[0]
        dy = im.size[1] - cropsize[1]
        box = (int(0 + centering[0]*dx), 
               int(0 + centering[1]*dy), 
               int(im.size[0] - (1-centering[0])*dx), 
               int(im.size[1] - (1-centering[1])*dy))
        im = im.crop(box)
    return im.resize(size, method)
    #return ImageOps.fit(im, size, method=METHOD, centering=CENTERING)


def process(filename, destdir, type):
    # extract first page of PDFs as its image (but only if one wasn't provided)
    from subprocess import call
    if filename.endswith('.pdf'):
        name = filename[:-4]
        imagefile = '%s.jpg' % name
        if not os.path.exists(imagefile):
            call(['convert', '-density', '300', '%s.pdf[0]' % name, '%s.jpg' % name])

    # move original file
    perms = os.stat(filename).st_mode
    if not(perms & stat.S_IRUSR and perms & stat.S_IRGRP and perms & stat.S_IROTH):
        os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
    fullfilename = os.path.join(destdir, type, os.path.basename(filename))
    # print filename, fullfilename
    shutil.move(filename, fullfilename)
    return fullfilename


def processimage(filename, newname, destdir, res):

    if not newname.endswith('.jpg'):
        newname = newname + '.jpg'
    try:
        im = Image.open(filename)
        if im.mode != "RGB":
            im = im.convert("RGB")
    except IOError:
        print 'Error: cannot open %s' % filename
        return

    sizes = subset_sizes(res, im.size)
    if not sizes:
        print 'Error: no sizes for resource type %s' % res
        return

    im = presize(im, sizes)

    for (name, size) in sizes.iteritems():
        # print name

        # crop and resize
        im_out = imagecrop(im, size, method=METHOD, centering=CENTERING)

        # save file
        #os.makedirs(os.path.join(destdir, name))
        newfilename = os.path.join(destdir, name, newname)
        # if newfilename.endswith('.png'):
        #     newfilename = newfilename[:-3] + 'jpg'
        # if newfilename.endswith('.jpeg'):
        #     newfilename = newfilename[:-4] + 'jpg'
        # print newfilename
        im_out.save(os.path.join(destdir, name, newname), quality=90)


# def main():
#     # if len(sys.argv) > 1:
#     #     reinit_reprocess()
#     #     global RESOURCES
#     #     RESOURCES = {'images': {'formats': ['thumb_android']}}

#     #lockfile = os.path.normpath(tempfile.gettempdir() + '/djangoplicity_image_processing.lock')
#     lock = FileLock(LOCKFILE)

#     try:
#         # make sure there is only one instance of the script running
#         lock.acquire(timeout=0)
#         i = 0
#         if os.path.isfile(DATAFILE):
#             fdata = open(DATAFILE)
#             data = json.load(fdata)
#             fdata.close()
#         else:
#             data = {}

#         for res in RESOURCES.keys():
#             srcdir = os.path.join(SRCDIR, res)
#             if REPROCESS:
#                 srcdir = os.path.join(srcdir, 'original')
#             destdir = os.path.join(DESTDIR, res)

#             files = glob.glob(os.path.join(srcdir, '*'))  # this won't return hidden files
#             # we want to do images last; this way, if someone provides a jpg for use as a cover for their
#             # pdf, the provided jpg will overwrite the generated jpg
#             imgfiles = []
#             for f in files:
#                 if f.endswith('.jpg'):
#                     imgfiles.append(f)
#             for f in imgfiles:
#                 files.remove(f)
#                 files.append(f)

#             for f in files:
#                 if os.path.isfile(os.path.join(srcdir, f)):
#                     i += 1
#                     size = os.path.getsize(f)
#                     if size > data.get(f, -1):
#                         # file is still being saved; skip it
#                         data[f] = size
#                     else:
#                         # file is ready
#                         if filetype_match(f, IMGTYPES):
#                             print 'image:', f
#                             processimage(f, destdir, res)
#                             if not KEEPFILE:
#                                 if f.endswith('.png'):
#                                     fullfilename = process(f, destdir, 'png')
#                                 else:
#                                     fullfilename = process(f, destdir, 'original')
#                         elif filetype_match(f, OTHERTYPES) and folder_exists_for(f, destdir):
#                             print 'other:', f
#                             if not KEEPFILE:
#                                 fullfilename = process(f, destdir, os.path.splitext(f)[1][1:])
#                         else:
#                             print 'unsupported:', f
#                             if not KEEPFILE:
#                                 fullfilename = process(f, destdir, 'other')
#                         del data[f]

#         # make sure there is some time until the next time this script is run
#         if i > 0:
#             print data
#             fdata = open(DATAFILE, 'w')
#             data = json.dump(data, fdata)
#             fdata.close()
#             time.sleep(SLEEPTIME)
#     except AlreadyLocked:
#         # another instance is already running. quit.
#         print 'Already Locked'
#         pass
#     finally:
#         if lock.is_locked():
#             lock.release()


# if __name__ == '__main__':
#     main()
