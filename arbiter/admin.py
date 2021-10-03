from django.contrib import admin
from .models import ArbiterProfile, Court, Language, Specialization, Location
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse


class LanguageInline(admin.TabularInline):
    model = Language.arbiter.through


class SpecializationInline(admin.TabularInline):
    model = Specialization.arbiter.through


class ArbiterProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "get_name", "verified", "email", "nationality", "active")
    filter_horizontal = ("specializations",)

    def get_name(self, obj):
        name = "None"
        try:
            name = obj.user.get_full_name()
        except:
            pass
        return name

    get_name.short_description = "name"

    inlines = (LanguageInline, SpecializationInline)

def generate_random_arbiters(*args):
    return HttpResponseRedirect(reverse("get-arbiters-form"))

def load_real_arbiters(*args):
    return HttpResponseRedirect(reverse("load-arbiters"))


admin.site.register(ArbiterProfile, ArbiterProfileAdmin)
admin.site.register(Court)
admin.site.register(Language)
admin.site.register(Specialization)
admin.site.register(Location)
admin.site.add_action(generate_random_arbiters)
admin.site.add_action(load_real_arbiters)
