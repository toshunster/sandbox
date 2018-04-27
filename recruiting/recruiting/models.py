# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Company( models.Model ):
    name = models.CharField( max_length=256, blank=False, null=False )
    logo = models.CharField( max_length=512 )
    
    class Meta:
        verbose_name="company"
        verbose_name_plural="companies"

class City( models.Model ):
    name = models.CharField( max_length=256, blank=False, null=False )
    
    class Meta:
        verbose_name="city"
        verbose_name_plural="cities"

class Vacancy( models.Model ):
    is_active = models.BooleanField( default=False )
    starts_at = models.DateTimeField( auto_now_add = True )
    title = models.CharField( max_length=256 )
    description = models.TextField()
    company = models.ForeignKey( Company )
    location = models.ForeignKey( City )

    class Meta:
        verbose_name="vacancy"
        verbose_name_plural = "vacancies"
