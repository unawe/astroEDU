# from django.utils.timezone import now

from haystack import indexes

from astroedu.activities.models import Activity


class ActivityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # user = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='release_date')

    age = indexes.FacetMultiValueField()
    level = indexes.FacetMultiValueField()
    time = indexes.CharField(model_attr='time', faceted=True)
    group = indexes.CharField(model_attr='group', faceted=True, null=True)
    supervised = indexes.CharField(model_attr='supervised', faceted=True, null=True)
    cost = indexes.CharField(model_attr='cost', faceted=True, null=True)
    location = indexes.CharField(model_attr='location', faceted=True, null=True)
    skills = indexes.FacetMultiValueField()
    learning = indexes.CharField(model_attr='learning', faceted=True)

    def get_model(self):
        return Activity

    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated. Only index already published items.'''
        return self.get_model().objects.all()
        # return self.get_model().objects.filter(release_date__lte=now())

    def prepare_age(self, obj):
        return [md.title for md in obj.age.all()]

    def prepare_level(self, obj):
        return [md.title for md in obj.level.all()]

    def prepare_skills(self, obj):
        return [md.title for md in obj.skills.all()]

