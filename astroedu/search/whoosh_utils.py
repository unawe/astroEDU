from whoosh.fields import Schema, ID, TEXT, STORED, KEYWORD
from whoosh.columns import RefBytesColumn
from whoosh.qparser import QueryParser, MultifieldParser, WildcardPlugin
from whoosh.analysis import StemmingAnalyzer, CharsetFilter
from whoosh.sorting import Facets, StoredFieldFacet, FieldFacet
from whoosh.support.charset import accent_map
from django.conf import settings
from whoosh.analysis.morph import StemFilter

from django_ext.whoosh_utils import LanguageIndex
from activities.models import Activity


def _get_schema():
    analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)  # WARN: stemming is english specific
    schema = Schema(
        slug=ID(unique=True, stored=True),
        title=TEXT(analyzer=analyzer, stored=True),
        content=TEXT(analyzer=analyzer),
        keywords=KEYWORD(commas=True, lowercase=True, sortable=RefBytesColumn()),  # , scorable=True

        teaser=STORED(),
        theme=STORED(),
        age_range=STORED(),
        release_date=STORED(),
        author_list=STORED(),
        code=STORED(),
        main_visual=STORED(),
        is_released=STORED(),

        age=KEYWORD(commas=True, sortable=RefBytesColumn()),
        level=KEYWORD(commas=True, sortable=RefBytesColumn()),
        time=ID(sortable=RefBytesColumn(), stored=True),
        group=ID(sortable=RefBytesColumn()),
        supervised=ID(sortable=RefBytesColumn()),
        cost=ID(sortable=RefBytesColumn()),
        location=ID(sortable=RefBytesColumn()),
        skills=KEYWORD(commas=True, sortable=RefBytesColumn()),
        learning=ID(sortable=RefBytesColumn()),
    )
    return schema


def _content(obj):
    # TODO: should run through markdown to remove markup...
    return '\n\n\n'.join([
        # obj.title,
        obj.theme,
        obj.teaser,
        obj.description,
        # obj.keywords,
        obj.materials,
        obj.goals,
        obj.objectives,
        obj.background,
        obj.fulldesc,
        obj.evaluation,
        obj.curriculum,
        obj.additional_information,
        obj.conclusion,
    ])


def _optimize_analyzer(writer):
    # optimize analyzer for batch updates
    analyzer = writer.schema['content'].analyzer
    for item in analyzer.items:
        if isinstance(item, StemFilter):
            item.cachesize = -1
            item.clear()


def rebuild_indexes():
    try:
        writers = {}
        # print("rebuild_indexes")
        for obj_master in Activity.objects.available():
            for obj in obj_master.translations.all():
                lang = obj.language_code
                if lang not in writers:
                    ix = LanguageIndex(settings.WHOOSH_INDEX_PATH, lang, _get_schema())
                    ix.clear()
                    writers[lang] = ix.get_writer()
                    _optimize_analyzer(writers[lang])
                # print(obj)
                _update_activity(obj_master, obj, writer=writers[lang])
    finally:
        for writer in writers.values():
            writer.commit()


def _update_activity(obj_master, obj, writer):
    writer.update_document(
        slug=obj.slug, title=obj.title, content=_content(obj),
        keywords=obj.keywords,

        teaser=obj.teaser,
        theme=obj.theme,
        age_range=obj_master.age_range(),
        release_date=obj_master.release_date,
        author_list=obj_master.author_list(),
        code=obj_master.code,
        main_visual=obj_master.main_visual,
        is_released=obj_master.is_released(),

        age=u','.join([x.code for x in obj_master.age.all()]),
        level=u','.join([x.code for x in obj_master.level.all()]),
        time=obj_master.time.code if obj_master.time else None,
        group=obj_master.group.code if obj_master.group else None,
        supervised=obj_master.supervised.code if obj_master.supervised else None,
        cost=obj_master.cost.code if obj_master.cost else None,
        location=obj_master.location.code if obj_master.location else None,
        skills=u','.join([x.code for x in obj_master.skills.all()]),
        learning=obj_master.learning.code if obj_master.learning else None,
    )


def update_article(obj_master):
    indexes = LanguageIndexes()
    for obj in obj_master.translations.all():
        with indexes[obj.language_code].get_writer() as writer:
            _update_activity(obj_master, obj, writer=writer)


def remove_activity(obj):
    #TODO
    pass

# def _comma_split(text):
#     if text:
#         result = text.split(',')
#         result = [x.strip() for x in result]
#     else:
#         result = None
#     return result


def search(querystring, language_code, queryfacets=None):
    ix = LanguageIndex(settings.WHOOSH_INDEX_PATH, language_code, _get_schema()).load()
    # parser = QueryParser('content', ix.schema)
    parser = MultifieldParser(['title', 'keywords', 'content'], ix.schema)  # fieldboosts={'title':5, 'keywords':4, 'content':1})
    parser.remove_plugin_class(WildcardPlugin)  # remove unused feature for better performance
    query = parser.parse(querystring)

    facets = Facets()
    ## StoredFieldFacet makes maerged groups; to use, don't forget to add `stored=True` to schema definition
    # facets.add_facet('keywords', StoredFieldFacet('keywords', allow_overlap=True, split_fn=_comma_split))
    facets.add_field('keywords', allow_overlap=True)
    facets.add_field('supervised')
    facets.add_field('cost')
    facets.add_field('location')
    facets.add_field('age', allow_overlap=True)
    facets.add_field('level', allow_overlap=True)
    facets.add_field('time')
    facets.add_field('group')
    facets.add_field('supervised')
    facets.add_field('cost')
    facets.add_field('location')
    facets.add_field('skills', allow_overlap=True)
    facets.add_field('learning')

    result = {
        'results': [],
        'facets': {'fields': {}},
    }

    with ix.searcher() as searcher:
        results = searcher.search(query, groupedby=facets)
        # import pdb; pdb.set_trace()

        # collect facets filters
        hit_filter = []
        for facet_name in results.facet_names():
            if facet_name in queryfacets:
                facet_value = queryfacets[facet_name]
                if facet_value:
                    hit_filter.append(results.groups(facet_name)[facet_value])

        # calculate intersection of all query facets
        if hit_filter:
            hit_filter = set.intersection(*[set(x) for x in hit_filter])

        # collect results
        for hit in results:
            if not hit_filter or hit.docnum in hit_filter:
                my_hit = {}
                # my_hit['pos'] = hit.pos
                # my_hit['rank'] = hit.rank
                # my_hit['docnum'] = hit.docnum
                my_hit['score'] = hit.score
                my_hit['object'] = hit.fields()
                my_hit['object']['is_visible'] = True
                result['results'].append(my_hit)
                # print hit.pos, hit.rank, hit.docnum, hit.score, hit.fields()['age_range'], hit

        # collect facets
        for facet_name in results.facet_names():
            result['facets']['fields'][facet_name] = []
            for facet_value, doc_list in results.groups(facet_name).items():
                if facet_value:
                    # filter by query facets
                    if hit_filter:
                        doc_list = set.intersection(set(doc_list), hit_filter)
                    if doc_list:
                        if facet_name in queryfacets and queryfacets[facet_name] and queryfacets[facet_name] != facet_value:
                            # for selected facets, only collect the selected option!
                            pass
                        else:
                            # get facet totals instead of document IDs
                            result['facets']['fields'][facet_name].append((facet_value, len(doc_list), ))

    return result
