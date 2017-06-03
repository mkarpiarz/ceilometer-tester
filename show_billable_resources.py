#!/usr/bin/env python
import os
from keystoneauth1.identity import v3
from keystoneauth1 import session
#import ceilometerclient.client
import ceilomarius

def main():
    if not os.environ.get('OS_CEILOMETER_URL'):
        print("ERROR: $OS_CEILOMETER_URL variable not set!")
        print("Use this as an example: OS_CEILOMETER_URL=https://compute.datacentred.io:8777")
        exit(1)

    # get a token
    auth = v3.Password(auth_url=os.environ['OS_AUTH_URL'],
                       username=os.environ['OS_USERNAME'],
                       password=os.environ['OS_PASSWORD'],
                       project_name=os.environ['OS_PROJECT_NAME'],
                       user_domain_id='default',
                       project_domain_id='default')
    sess = session.Session(auth=auth)
    token = auth.get_token(sess)

    # use the token with ceilometer's endpoint
    # NOTE: Sadly, the official client doesn't seem to work with the `limit` parameter.
    # NOTE: Use the new custom class.
    #
    #cclient = ceilometerclient.client.get_client(2,
    #                           os_endpoint=os.environ['OS_CEILOMETER_URL'],
    #                           os_token=token)
    #query_samples = [dict(field='meter', op='eq', value='instance')]
    #print( cclient.samples.list( q=query_samples, limit=1 ) )
    ceilomar = ceilomarius.Ceilomarius(api_version=2,
                                        endpoint=os.environ['OS_CEILOMETER_URL'],
                                        token=token,
                                        verbose = True)
    query = [{"field": "meter", "op": "eq", "value": "instance"}]
    print( ceilomar.get_samples(q=query, limit=1) )

if __name__ == "__main__":
    main()
