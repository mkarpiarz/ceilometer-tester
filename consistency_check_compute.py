import paginator
import mongor
from datetime import datetime, timedelta
import argparse
import credentials
import config

def compare_samples(samples_api, samples_db, verbose=False):
    # First compare sizes of lists with samples
    len_api = len(samples_api)
    len_db = len(samples_db)
    if verbose:
        print( "INFO: Number of samples from API: {}".format(len_api) )
        print( "INFO: Number of samples from the database: {}".format(len_db) )

    if len_api == len_db:
        print( "INFO: [SUCCESS] Numbers of samples ({}) match!".format(len_db) )
    else:
        print( "WARNING: [FAILURE] Number of samples from API ({}) and from the database {} don't match.".format(len_api, len_db) )

    # Prepare a dictionary for samples from API
    dict_samples_api = {}
    for i in xrange( 0, len(samples_api) ):
        dict_samples_api[samples_api[i]['message_id']] = i
    print( len(dict_samples_api) )

    # Go through the list of samples from the database
    # and check which ones are not in the dict from API
    # (also stores the dict of samples from db for reference)
    dict_samples_db = {}
    missing_in_api = []
    for i in xrange( 0, len(samples_db) ):
        if not dict_samples_api.get(samples_db[i]['message_id']):
            missing_in_api.append(samples_db[i])
        dict_samples_db[samples_db[i]['message_id']] = i
    print( len(dict_samples_db) )

    print( "INFO: Number of samples missing in the api: {}".format(len(missing_in_api)) )
    if verbose:
        print("INFO: Here are the missing items:")
        print(missing_in_api)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_id", help="Instance ID to compare samples for.")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    instance_id = args.instance_id

    verbose = False
    if args.verbose:
        print("INFO: Verbosity turned on.")
        verbose = True

    print("INFO: This will compare 2 weeks worth of samples for specified instance.")

    # get a token
    creds = credentials.Credentials()
    token = creds.get_token()

    # get config
    conf = config.Config()

    pag = paginator.Paginator(endpoint = conf.ceilometer_endpoint, token = token)
    mon = mongor.Mongor()

    time_end = datetime.utcnow()
    time_begin = time_end - timedelta(days=14)

    samples_api = pag.get_samples_for_instance(instance_id, time_begin, time_end)
    samples_db = mon.get_samples_for_instance(instance_id, time_begin, time_end)

    compare_samples(samples_api, samples_db, verbose)

if __name__ == "__main__":
    main()
