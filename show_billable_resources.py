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
    # stores every meter associated with resources from this stack
    meters_all = dict()
    for res in resources:
        if verbose:
            print( "INFO: Retrieved resource: %s" % res)
        meters_all.update( ceilomar.get_meters_for_resource(res, limit=1) )
    if verbose:
        for key in meters_all.keys():
            print( "INFO: All meters retrieved from the stack:")
            print( "INFO: The main key: %s" % key )
            print( "INFO: Values for this key:" )
            for item in meters_all.get(key):
                print( "INFO: counter_name: {}, resource_id: {}, timestamp: {}".format( item.get('counter_name'), item.get('resource_id'), item.get('timestamp') ) )

    # variables for stats on the number of found meters
    n_required = 0
    n_found = 0
    # read required meters from a file
    with open('required_meters.txt', 'r') as f:
        for line in f:
            meter = line.strip()
            if meter in meters_all:
                for item in meters_all[meter]:
                    print( "meter: {meter} -> timestamp: {timestamp}".format(meter=item.get('counter_name'), timestamp=item.get('timestamp')) )
                    if verbose:
                        print( "INFO: Resource metadata:" )
                        print( "INFO: {}".format(item.get('resource_metadata')) )
                n_found += 1
            n_required += 1

    print( "Found {} out of all {} meters!".format(n_found, n_required) )

if __name__ == "__main__":
    main()
