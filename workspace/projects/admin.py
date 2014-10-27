from django.contrib import admin
from .models import Needed, UserProfile
# Register your models here.
class NeededAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'uuid', 'posted', 'likes']
	class Meta:
		model = Needed
admin.site.register(Needed, NeededAdmin)
admin.site.register(UserProfile)
