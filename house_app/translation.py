from .models import (Property,Region,City,District)
from modeltranslation.translator import TranslationOptions,register

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description','address')

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region_name',)

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('district_name',)