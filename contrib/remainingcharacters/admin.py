from django.contrib import admin

# source: https://github.com/broderboy/django-admin-remainingcharacters/blob/master/remainingcharacters/admin.py

#have your ModelAdmin inherit this to use
class CounterAdmin(admin.ModelAdmin):
    counted_fields = ()
    
    #really for textareas
    max_lengths = {'abstract': 400,}
    
    class Media:
        js = (
              'http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js',
              'js/jquery.charCount.js',
              )
        
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(CounterAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        # print db_field.name
        # print self.counted_fields
        if db_field.name in self.counted_fields:
            try:
                len = self.max_lengths[db_field.name]
                field.widget.attrs['maxlength'] = len
            except: pass
            field.widget.attrs['class'] = 'counted ' + field.widget.attrs.get('class','')
        return field

