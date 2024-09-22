import googlemaps

class GeocodeFetcher:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def get_geocode(self, address):
        res = self.gmaps.geocode(address)
        if res:
            location = res[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None, None