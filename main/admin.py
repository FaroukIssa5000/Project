from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(Engneer)
admin.site.register(Contractor)
admin.site.register(Craftman)
admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(Project)
admin.site.register(CatogaryEngneerForProject)
admin.site.register(CatogaryCraftmanForProject)

# # Register your models here.
