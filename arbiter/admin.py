from django.contrib import admin
from .models import ArbiterProfile, Court, Language, Experience, Specialization, Location
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse


class LanguageInline(admin.TabularInline):
    model = Language.arbiter.through


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0


class SpecializationInline(admin.TabularInline):
    model = Specialization.arbiter.through


class ArbiterProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "get_name", "verified", "email", "nationality", "active", "get_experience")
    filter_horizontal = ("specializations",)

    def get_name(self, obj):
        name = "None"
        try:
            name = obj.user.get_full_name()
        except:
            pass
        return name

    def get_experience(self, obj):
        return obj.experience.aggregate(Sum("period"))['period__sum']

    get_name.short_description = "name"
    get_experience.short_description = "Months of experience"

    inlines = (LanguageInline, ExperienceInline, SpecializationInline)

def generate_random_arbiters(*args):
    return HttpResponseRedirect(reverse("get-arbiters-form"))


admin.site.register(ArbiterProfile, ArbiterProfileAdmin)
admin.site.register(Court)
admin.site.register(Language)
admin.site.register(Experience)
admin.site.register(Specialization)
admin.site.register(Location)
admin.site.add_action(generate_random_arbiters)
