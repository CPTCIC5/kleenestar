from django.contrib import admin
from . import models


admin.site.register(models.Campaign)
admin.site.register(models.AdSet)
admin.site.register(models.Ads)
admin.site.register(models.PerformanceMetric)
admin.site.register(models.AudienceDemographics)
admin.site.register(models.SentimentAnalysis)