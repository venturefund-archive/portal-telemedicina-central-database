from modeltranslation.translator import TranslationOptions, register

from .models import HistoricalVaccineAlertType, VaccineAlertType


@register(VaccineAlertType)
class VaccineAlertTypeTranslationOptions(TranslationOptions):
    fields = ["description"]
    required_languages = ("en", "pt-br")


@register(HistoricalVaccineAlertType)
class HistoricalVaccineAlertTypeTranslationOptions(TranslationOptions):
    fields = ["description"]
    required_languages = ("en", "pt-br")
