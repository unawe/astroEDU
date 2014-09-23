from astroedu.activities.models import MetadataOption


def add(group, code, title, position):
    x = MetadataOption(group=group, code=code, title=title, position=position)
    x.save()



i = 0
i+=1; add('age', '0-4', u'0 > 4', i)
i+=1; add('age', '4-6', u'4 > 6', i)
i+=1; add('age', '6-8', u'6 > 8', i)
i+=1; add('age', '8-10', u'8 > 10', i)
i+=1; add('age', '10-12', u'10 > 12', i)
i+=1; add('age', '12-14', u'12 > 14', i)
i+=1; add('age', '14-16', u'14 > 16', i)
i+=1; add('age', '16-19', u'16 > 19', i)
i+=1; add('age', '19plus', u'19+', i)
i = 0
i+=1; add('time', '15min', u'15min', i)
i+=1; add('time', '30min', u'30min', i)
i+=1; add('time', '45min', u'45min', i)
i+=1; add('time', '1h', u'1h', i)
i+=1; add('time', '1h30', u'1h30', i)
i+=1; add('time', '2h', u'2h', i)
i+=1; add('time', '3h', u'3h', i)
i+=1; add('time', '12h', u'1/2 day', i)
i+=1; add('time', '24h', u'1 day', i)
i = 0
i+=1; add('level', 'pre', u'Pre-school', i)
i+=1; add('level', 'primary', u'Primary School', i)
i+=1; add('level', 'middle', u'Middle School', i)
i+=1; add('level', 'secondary', u'Secondary School', i)
i+=1; add('level', 'university', u'University', i)
i+=1; add('level', 'informal', u'Informal', i)
i = 0
i+=1; add('group', 'individual', u'Individual', i)
i+=1; add('group', 'group', u'Group', i)
i = 0
i+=1; add('supervised', 'supervised', u'Supervised', i)
i+=1; add('supervised', 'unsupervised', u'Unsupervised', i)
i = 0
i+=1; add('cost', 'low', u'Low (< ~5 EUR)', i)
i+=1; add('cost', 'average', u'Average  (5 - 25 EUR)', i)
i+=1; add('cost', 'expensive', u'Expensive (> 25 EUR)', i)
i = 0
i+=1; add('location', 'indoors_small', u'Indoors (small, e.g. classroom)', i)
i+=1; add('location', 'indoors_large', u'Indoors (small, e.g. school hall)', i)
i+=1; add('location', 'outdoors', u'Outdoors', i)
i = 0
i+=1; add('skills', 'problem_solving', u'Problem solving', i)
i+=1; add('skills', 'visual_interpretation', u'Visual interpretation', i)
i+=1; add('skills', 'presentation_discoveries', u'Presentation of discoveries', i)
i = 0
i+=1; add('learning', 'open-ended', u'Open-ended enquiry', i)
i+=1; add('learning', 'guided', u'Guided enquiry', i)
i+=1; add('learning', 'structured', u'Structured enquiry', i)
i+=1; add('learning', 'confirmation_verification', u'Confirmation or Verification', i)

