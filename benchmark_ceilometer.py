import os
import credentials
import ceilomarius

def main():
    if not os.environ.get('OS_CEILOMETER_URL'):
        print("ERROR: $OS_CEILOMETER_URL variable not set!")
        print("Use this as an example: OS_CEILOMETER_URL=https://compute.datacentred.io:8777")
        exit(1)

    # get a token
    creds = credentials.Credentials()
    token = creds.get_token()

    ceilomar = ceilomarius.Ceilomarius(api_version = 2,
                                        endpoint = os.environ['OS_CEILOMETER_URL'],
                                        token = token,
                                        verbose = False)

    query = [{'field': 'metadata.event_type', 'op': 'eq', 'value': 'compute.instance.exists'}]
    for l in xrange(1,11):
        for iter in xrange(1,6):
            resp = ceilomar.get_metric(meter_name="instance", q=query, limit=l)
            objects = resp.json()
            print("Objects retrieved: {}, us elapsed: {}, try no: {}".format(len(objects), resp.elapsed.microseconds, iter) )

if __name__ == "__main__":
    main()
