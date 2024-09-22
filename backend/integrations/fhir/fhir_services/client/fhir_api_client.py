import logging
import json
import requests
from typing import Dict, Any, List
from urllib.parse import urlparse, parse_qs
from fhir.resources.R4B.bundle import Bundle, BundleEntry
from datetime import date


from .setup.base.fhir_api_setup import FHIRAPISetup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

class FHIRAPIClient:
    def __init__(self, setup: FHIRAPISetup):
        self.base_url = setup.get_base_url()
        self.session = setup.get_session()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # logger.error(f"Error making {method} request to {endpoint}: {str(e)}")
            raise RuntimeError(f"FHIR API request failed: {str(e)}")
    
    def create_resource(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        resource_type = resource.get('resourceType')
        
        if not resource_type:
            raise ValueError("Resource must have a 'resourceType' field")
        
        logger.info(f"Creating new {resource_type} resource")
        endpoint = resource_type
        print(resource)
        json_data = json.dumps(resource, cls=JSONEncoder)
        return self._make_request("POST", endpoint, data=json_data, headers={'Content-Type': 'application/json'})

    def update_resource(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        resource_type = resource.resource_type
        resource_id = resource.id
        
        if not resource_type or not resource_id:
            raise ValueError("Resource must have both 'resourceType' and 'id' fields")
        
        logger.info(f"Updating {resource_type} resource with ID: {resource_id}")
        endpoint = f"{resource_type}/{resource_id}"
        
        return self._make_request("PUT", endpoint, json=json.loads(resource.json()))

    
    def get_resource(self, resource_type: str, resource_id: str) -> Dict[str, Any]:
        endpoint = f"{resource_type}/{resource_id}"
        logger.info(f"Fetching {resource_type} resource with ID: {resource_id}")
        return self._make_request("GET", endpoint)

    def update_resources_in_bundle(self, resources: List[Any], bundle_type: str = "transaction") -> Dict[str, Any]:
        entries = []

        for resource in resources:
            entry = BundleEntry(
                resource=resource,
                request={
                    "method": "PUT",
                    "url": f"{resource.resource_type}/{resource.id}"
                }
            )
            entries.append(entry)

        bundle = Bundle(type=bundle_type, entry=entries)
        logger.info(f"Submitting bundle with {len(entries)} entries")
        return self._make_request("POST", "", json=json.loads(bundle.json()))
    
    def search_resources(self, resource_type: str, search_params: Dict[str, Any] = None) -> Dict[str, Any]:
        # logger.info(f"Searching for {resource_type} resources with params: {search_params}")
        return self._make_request("GET", resource_type, params=search_params)

    def fetch_all_pages_resources(self, resource_type: str, search_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        logger.info(f"Fetching all {resource_type} resources with params: {search_params}")
        all_resources = []
        next_page_token = None

        while True:
            params = search_params or {}
            params["_count"] = 1000 
            if next_page_token:
                params["_page_token"] = next_page_token

            bundle = self._make_request("GET", resource_type, params=params)
            all_resources.extend([entry['resource'] for entry in bundle.get('entry', [])])

            next_link = next((link for link in bundle.get('link', []) if link.get('relation') == 'next'), None)
            if next_link and 'url' in next_link:
                parsed_url = urlparse(next_link['url'])
                query_params = parse_qs(parsed_url.query)
                next_page_token = query_params.get('_page_token', [None])[0]
            else:
                next_page_token = None

            if not next_page_token:
                break

        return all_resources
