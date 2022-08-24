from glob import glob

import requests

if __name__ == "__main__":
    url = "http://localhost:8080/fhir"
    headers = {
        "Accept": "application/fhir+json",
        "Content-Type": "application/fhir+json",
    }

    hospital_bundles = glob("./fhir/hospitalInformation*.json")
    practitioner_bundles = glob("./fhir/practitionerInformation*.json")
    patient_bundles = glob("./fhir/*_*_*.json")

    # bundles must be uploaded in this order
    # reason: https://github.com/synthetichealth/synthea/wiki/FHIR-Transaction-Bundles # noqa
    for bundle in [*hospital_bundles, *practitioner_bundles, *patient_bundles]:
        r = requests.post(url, data=open(bundle, "rb"), headers=headers)
        print(r.status_code)
