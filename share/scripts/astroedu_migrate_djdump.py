import json

INPUT = '/tmp/astroedu_djdump.json'
OUTPUT = '/tmp/astroedu_djdump_next.json'


def skip(item):
    return []


def transform_flatpage(item):
    print(item['model'])
    model = 'smartpages.smartpage'
    master = {}
    trans = {}
    for name, value in item['fields'].items():
        if name in ['url', 'title', 'content', ]:
            trans[name] = value
        elif name in ['template_name', 'sites', 'enable_comments', ]:
            pass
        else:
            print('  %s' % name)
            master[name] = value
    master['code'] = item['fields']['url'][1:-1]
    master['featured'] = False
    master['published'] = True
    master['release_date'] = "2000-01-01T00:00:00Z"
    trans['master'] = item['pk']
    trans['language_code'] = 'en'

    return [
        {'model': model, 'pk': item['pk'], 'fields': master, },
        {'model': model + 'translation', 'fields': trans, },
    ]


def transform_institution(item):
    print(item['model'])
    model = 'institutions.institution'
    master = {}
    trans = {}
    location = {}
    for name, value in item['fields'].items():
        if name in ['country', ]:
            location[name] = value
        elif name in ['logo', ]:
            pass
        else:
            print('  %s' % name)
            master[name] = value
    # location['city'] = ''
    master['location'] = item['pk']
    # master['fullname'] = ''  # master['name']
    # master['spacescoop_count'] = -1
    trans['master'] = item['pk']
    trans['language_code'] = 'en'

    return [
        {'model': 'institutions.location', 'pk': item['pk'], 'fields': location, },
        {'model': model, 'pk': item['pk'], 'fields': master, },
        {'model': model + 'translation', 'fields': trans, },
    ]


def transform_author(item):
    print(item['model'])
    item['model'] = 'institutions.person'
    return [item]


def transform_activity(item):
    print(item['model'])
    model = item['model']
    master = {}
    trans = {}
    for name, value in item['fields'].items():
        if name in ['slug', 'title', 'teaser', 'theme', 'keywords', 'acknowledgement', 'description', 'goals', 'objectives', 'evaluation', 'materials', 'background', 'fulldesc', 'curriculum', 'additional_information', 'conclusion', ]:
            trans[name] = value
        elif name == 'lang':
            trans['language_code'] = value
        else:
            print('  %s' % name)
            master[name] = value
    trans['master'] = item['pk']
    return [
        {'model': model, 'pk': item['pk'], 'fields': master, },
        {'model': model + 'translation', 'fields': trans, },
    ]


def transform_collection(item):
    print(item['model'])
    model = item['model']
    master = {}
    trans = {}
    for name, value in item['fields'].items():
        if name in ['slug', 'title', 'description', ]:
            trans[name] = value
        elif name == 'lang':
            pass
        else:
            print('  %s' % name)
            master[name] = value
    trans['master'] = item['pk']
    trans['language_code'] = 'en'
    return [
        {'model': model, 'pk': item['pk'], 'fields': master, },
        {'model': model + 'translation', 'fields': trans, },
    ]


def transform_repositoryentry(item):
    REPOS = {
        'Scientix': 1,
        'OER': 2,
        'TES': 3,
        '': None,
    }
    print(item['model'])
    item['fields']['repo'] = REPOS[item['fields']['repo']]
    return [item]


def transform_logentry(item):
    CTYPES = {
        'flatpages.flatpage': 'smartpages.smartpage',
        'activities.institution': 'institutions.institution',
        'activities.author': 'institutions.person',
    }
    print(item['model'])
    content_type = '.'.join(item['fields']['content_type'])
    if content_type in CTYPES:
        print('  %s -> %s' % (content_type, CTYPES[content_type], ))
        item['fields']['content_type'] = CTYPES[content_type].split('.')
    return [item]

TRANSFORMS = {
    'flatpages.flatpage': transform_flatpage,
    'activities.activity': transform_activity,
    'activities.institution': transform_institution,
    'activities.author': transform_author,
    'activities.collection': transform_collection,
    'activities.repositoryentry': transform_repositoryentry,
    # 'admin.logentry': skip,
    'admin.logentry': transform_logentry,
}


def transform(item):
    result = []
    f = TRANSFORMS.get(item['model'])
    if f:
        result += f(item)
    else:
        result.append(item)
    return result


if __name__ == "__main__":
    with open(INPUT) as f:
        data = json.load(f)

    new_data = []
    for item in data:
        new_items = transform(item)
        for new_item in new_items:
            new_data.append(new_item)

    with open(OUTPUT, 'w') as f:
        json.dump(new_data, f, indent=2)
