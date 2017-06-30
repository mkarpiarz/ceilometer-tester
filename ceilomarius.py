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
            print( "INFO: Got the response: {} [{}] on {}".format(req.status_code, req.reason, req.headers.get('date')) )
            print( "INFO: Your request ID: %s" % req.headers.get('x-openstack-request-id') )
            print( "INFO: The whole operation took: %s [h:m:s.us]" % req.elapsed )

        return req

    def get_meters_for_resource(self, resource, limit = 10):
        # skip those weird resources with empty IDs
        if not resource.id:
            if self.verbose:
                print( "WARNING: Wrong resource ID {}. Skipping.".format(resource.id) )
            return {}

        headers = self.prepare_headers()
        url = self.endpoint + '/v' + str(self.api_version) + '/resources/' + str(resource.id)
        resp = requests.get(url = url, headers = headers)

        # get a list of dicts with urls to meters:
        links = resp.json().get('links')

        if self.verbose:
            print( "INFO: Links associated with url %s:" % url )
            print( links )

        # check whether we have get meters
        if links:
            query = [{"field": "resource_id", "op": "eq", "value": str(resource.id)}]
            # this dict will store responses associated with the specific meter name
            meters = dict()
            for link in links:
                # the name of the meter can be retrieved from the 'rel' key
                rel = link.get('rel')
                # ignore the reference to the original url (where rel == 'self'):
                if rel != 'self':
                    meters[rel] = self.get_metric(meter_name=rel, q=query, limit=limit).json()
            return meters
        else:
            if self.verbose:
                print( "WARNING: Empty list of links! Skipping the resource." )
            return {}

    def get_statistics(self, meter_name, q = [], count_only = False):
        """Returns statistics for a given query q

        Arguments:
        count_only -- set to True to only return the number of records.
        """
        query = {}
        headers = self.prepare_headers()
        if q:
            query["q"] = q
        url = self.endpoint + '/v' + str(self.api_version) + '/meters/' + meter_name + ('/statistics?aggregate.func=count' if count_only else '/statistics')
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

def main():
    ceilo = Ceilomarius(api_version = 2,
                        endpoint = os.environ['OS_CEILOMETER_URL'],
                        token = os.environ['OS_TOKEN'],
                        verbose = True)

    query = [{"field": "metadata.event_type", "op": "eq", "value": "compute.instance.exists"}]
    print( ceilo.get_metric(meter_name="instance", q=query, limit=1).json() )

    print( ceilo.get_statistics(meter_name="instance", q=query).json() )

if __name__ == "__main__":
    main()
