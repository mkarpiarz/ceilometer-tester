import os
import credentials
#import ceilometerclient.client
import argparse

# Local libraries
import ceilomarius
import stacker
import resource

def main():
    if not os.environ.get('OS_CEILOMETER_URL'):
        print("ERROR: $OS_CEILOMETER_URL variable not set!")
        print("Use this as an example: OS_CEILOMETER_URL=https://compute.datacentred.io:8777")
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("stack_id", help="The ID or name of the stack with resources.")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    verbose = False
    if args.verbose:
        print("INFO: Verbosity turned on.")
        verbose = True

    # get a token
    creds = credentials.Credentials()
    token = creds.get_token()

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
                                        verbose=verbose)

    stack_id = args.stack_id
    stack = stacker.Stacker()
    resources = stack.get_resources_in_stack(stack_id)
    for res in resources:
        print res
        print( ceilomar.get_meters_for_resource(res) )

    exit(0)

    # read queries from a file
    with open('queries.txt', 'r') as f:
        header_line = f.readline()
        for line in f:
            query = []
            (meter_name, limit, query_params) = line.strip().split('\t')
            query_elems = query_params.split(',')
            for item in query_elems:
                (field, value) = item.split('=')
                query.append({"field": field, "op": "eq", "value": value})
            resp = ceilomar.get_metric(meter_name=meter_name, q=query, limit=int(limit))
            if verbose:
                print("DEBUG: The response:")
                print( resp.json() )
            for item in resp.json():
                print( "meter: {meter},  resource_id: {resource_id}\nquery: {query}\ntimestamp: {timestamp}".format( meter=meter_name, resource_id=item.get('resource_id'), query=query, timestamp=item.get('timestamp') ) )

if __name__ == "__main__":
    main()
