import os
import requests

class Ceilomarius:
    def __init__(self, api_version, endpoint, token, verbose):
        self.api_version = api_version
        self.endpoint = endpoint
        self.token = token
        self.verbose = verbose

    def prepare_headers(self):
        return {'User-Agent': 'ceilomarius',
                   'X-Auth-Token': str(self.token),
                   'Content-Type': 'application/json'}

    def get_metric(self, meter_name, q = [], limit = 10):
        headers = self.prepare_headers()
        query = {"limit": limit}
        if q:
            query["q"] = q
        url = self.endpoint + '/v' + str(self.api_version) + '/meters/' + meter_name
        if self.verbose:
            print( "INFO: Parameters of the request:" )
            print( "INFO: > url: %s" % url )
            print( "INFO: > headers: %s" % headers )
            print( "INFO: > query: %s" % query )

        req = requests.get(url = url, json = query, headers = headers)

        if self.verbose:
            print( "INFO: Got the response: {} [{}] at {}".format(req.status_code, req.reason, req.headers.get('date')) )
            print( "INFO: Your request ID: %s" % req.headers.get('x-openstack-request-id') )
            print( "INFO: The whole operation took: %s [h:m:s.us]" % req.elapsed )

        return req

    def get_meters_for_resource(self, resource, limit = 10):
        headers = self.prepare_headers()
        url = self.endpoint + '/v' + str(self.api_version) + '/resources/' + str(resource.id)
        resp = requests.get(url = url, headers = headers)
        links = resp.json().get('links')
        if self.verbose:
            print( "INFO: Links associated with url %s:" % url )
            print( links )

def main():
    ceilo = Ceilomarius(api_version = 2,
                        endpoint = os.environ['OS_CEILOMETER_URL'],
                        token = os.environ['OS_TOKEN'],
                        verbose = True)

    query = [{"field": "metadata.event_type", "op": "eq", "value": "compute.instance.exists"}]
    print( ceilo.get_metric(meter_name="instance", q=query, limit=1).json() )

if __name__ == "__main__":
    main()
