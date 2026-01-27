from django.contrib import admin
from .models import  (UserProfile,Property,PropertyImage,Review,Region,City,District)
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

class CityInline(admin.TabularInline,TranslationInlineModelAdmin):
    model = City
    extra = 1

class  DistrictInline(admin.TabularInline,TranslationInlineModelAdmin):
    model = District
    extra = 1

@admin.register(City)
class CityAdmin(TranslationAdmin):
    inlines = [DistrictInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    inlines = [CityInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(PropertyImage)
admin.site.register(Review)
admin.site.register(District)

