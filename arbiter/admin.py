from django.contrib import admin
from .models import ArbiterProfile, Court, Language, Experience, Specialization
from django.db.models import Sum
from django.contrib.auth.models import User

class LanguageInline(admin.StackedInline):
    model = Language
    extra = 0


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0


class SpecializationInline(admin.TabularInline):
    model = Specialization.arbiter.through


class ArbiterProfileAdmin(admin.ModelAdmin):
    list_display = ("id","get_name","verified", "email", "nationality", "active", "get_experience")
    filter_horizontal = ("specializations",)

    def get_name(self, obj):
        return obj.user.get_full_name()

    def get_experience(self, obj):
        return obj.experience.aggregate(Sum("period"))['period__sum']

    get_name.short_description = "name"
    get_experience.short_description = "Months of experience"

    inlines = (LanguageInline, ExperienceInline, SpecializationInline)


admin.site.register(ArbiterProfile, ArbiterProfileAdmin)
admin.site.register(Court)
admin.site.register(Language)
admin.site.register(Experience)
admin.site.register(Specialization)
