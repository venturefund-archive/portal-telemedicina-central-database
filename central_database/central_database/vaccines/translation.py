from modeltranslation.translator import TranslationOptions, register

from .models import VaccineAlertType


@register(VaccineAlertType)
class VaccineAlertTypeTranslationOptions(TranslationOptions):
    fields = ["description"]
    required_languages = ("en", "pt-br")
