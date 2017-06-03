import os
import requests

class Ceilomarius:
    def __init__(self, api_version, endpoint, token, verbose):
        self.api_version = api_version
        self.endpoint = endpoint
        self.token = token
        self.verbose = verbose

    def get_samples(self, q = [], limit = 10):
        headers = {'User-Agent': 'ceilomariusclient',
                   'X-Auth-Token': str(self.token),
                   'Content-Type': 'application/json'}
        query = {"limit": limit}
        if q:
            query["q"] = q
        url = self.endpoint + '/v' + str(self.api_version) + '/samples'
        if self.verbose:
            print("URL: %s" % url)
            print("HEADERS: %s" % headers)
            print("QUERY: %s" % query)

        req = requests.get(url = url, json = query, headers = headers)
        return req.text

def main():
    ceilo = Ceilomarius(api_version = 2,
                        endpoint = os.environ['OS_CEILOMETER_URL'],
                        token = os.environ['OS_TOKEN'],
                        verbose = True)

    query = [{"field": "meter", "op": "eq", "value": "instance"}]
    print( ceilo.get_samples(q=query, limit=1) )

if __name__ == "__main__":
    main()
