from astroedu.activities.models import MetadataOption, Activity


def add(group, code, title, position):
    x = MetadataOption(group=group, code=code, title=title, position=position)
    x.save()


# skills
for a in Activity.objects.all_super():
    a.skills.all().delete()

#MetadataOption.objects.filter(group='skills').delete()

i = 0
i+=1; add('skills', 'A', u'A Asking questions', i)
i+=1; add('skills', 'B', u'B Developing and using models', i)
i+=1; add('skills', 'C', u'C Planning and carrying out investigations', i)
i+=1; add('skills', 'D', u'D Analysing and interpreting data', i)
i+=1; add('skills', 'E', u'E Using mathematics and computational thinking', i)
i+=1; add('skills', 'F', u'F Constructing explanations', i)
i+=1; add('skills', 'G', u'G Engaging in argument from evidence', i)
i+=1; add('skills', 'H', u'H Communicating information', i)

# learning
opt = MetadataOption.objects.filter(group='learning').filter(code='open-ended')[0]
opt.code = 'full'
opt.title = u'Full enquiry'
opt.save()
opt = MetadataOption.objects.filter(group='learning').filter(code='guided')[0]
opt.code = 'partial'
opt.title = u'Partial enquiry'
opt.save()
opt = MetadataOption.objects.filter(group='learning').filter(code='structured')[0]
opt.code = 'demonstration'
opt.title = u'Demonstration / Illustration'
opt.save()
opt = MetadataOption.objects.filter(group='learning').filter(code='confirmation_verification')[0]
opt.code = 'fun'
opt.title = u'Fun learning'
opt.save()

for a in Activity.objects.all_super():
    # skills
    a.learning = opt
    a.save()

