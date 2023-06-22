import factory.fuzzy
from faker import Faker
from fhirclient.models.address import Address
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.extension import Extension
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.humanname import HumanName
from fhirclient.models.patient import Patient


class LatitudeExtensionFactory(factory.Factory):
    class Meta:
        model = Extension

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        extension = model_class(*args, **kwargs)
        extension.url = "latitude"
        extension.valueDecimal = Faker().pyfloat(
            left_digits=2, right_digits=5, positive=True
        )
        return extension


class LongitudeExtensionFactory(factory.Factory):
    class Meta:
        model = Extension

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        extension = model_class(*args, **kwargs)
        extension.url = "longitude"
        extension.valueDecimal = Faker().pyfloat(
            left_digits=2, right_digits=5, positive=True
        )
        return extension


class ExtensionFactory(factory.Factory):
    class Meta:
        model = Extension

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        extension = model_class(*args, **kwargs)
        extension.url = "http://example.com/my-extension"
        extension.extension = [
            LatitudeExtensionFactory(),
            LongitudeExtensionFactory(),
        ]  # noqa: E501
        return extension


class AddressFactory(factory.Factory):
    class Meta:
        model = Address

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        address = model_class(*args, **kwargs)

        address.line = [Faker().pystr()]
        address.city = Faker().pystr()
        address.state = Faker().pystr()
        address.postalCode = Faker().pystr()
        address.country = Faker().pystr()
        address.extension = [ExtensionFactory()]
        return address


class HumanNameFactory(factory.Factory):
    class Meta:
        model = HumanName

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        human_name = model_class(*args, **kwargs)
        human_name.given = [Faker().pystr()]
        human_name.family = Faker().pystr()
        return human_name


class PatientFactory(factory.Factory):
    class Meta:
        model = Patient

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        patient = model_class(*args, **kwargs)
        patient.id = Faker().pystr()
        patient.name = [HumanNameFactory()]
        patient.birthDate = FHIRDate(Faker().date())
        patient.gender = "female"
        patient.telecom = [
            ContactPoint(
                {
                    "system": "phone",
                    "value": "(03) 5555 6473",
                    "use": "work",
                    "rank": 1,
                }  # noqa: E501
            )
        ]
        patient.maritalStatus = CodeableConcept(
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",  # noqa: E501
                        "code": "M",
                        "display": "Married",
                    }
                ],
                "text": "Getrouwd",
            }
        )
        patient.address = [AddressFactory()]
        return patient
