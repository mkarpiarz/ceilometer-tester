import paginator
import mongor
from datetime import datetime, timedelta
import argparse
import credentials
import config
import pprint
import collections

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
        message_id = samples_api[i].get('message_id')
        if message_id:
            dict_samples_api[message_id] = i
        else:
            if verbose:
                print("WARNING: Dropping a sample without a message ID:")
                pprint.pprint(samples_api[i])

    # Go through the list of samples from the database
    # and check which ones are not in the dict from API
    # (also stores the dict of samples from db for reference)
    dict_samples_db = {}
    missing_in_api = []
    for i in xrange( 0, len(samples_db) ):
        message_id = samples_db[i].get('message_id')
        if message_id:
            dict_samples_db[message_id] = i
            # if a sample with current message ID is not in the dict from the API, it's missing
            if dict_samples_api.get(message_id) is None:
                missing_in_api.append(samples_db[i])
        else:
            if verbose:
                print("WARNING: Dropping a sample without a message ID:")
                pprint.pprint(samples_db[i])

    print( "INFO: Number of samples missing in the api: {}".format(len(missing_in_api)) )
    if verbose:
        print("INFO: Here are the missing items:")
        print(missing_in_api)

def extract_events_from_samples(samples):
    """Extracts event-based samples from a list of samples.
    """
    # a list of event-based samples
    event_samples = []
    # a histogram of events
    events_hist = collections.defaultdict(int)

    for sample in samples:
        if sample.get('resource_metadata') and sample['resource_metadata'].get('event_type'):
            event_samples.append(sample)
            events_hist[sample['resource_metadata']['event_type']] += 1

    print("INFO: Histogram of events:")
    pprint.pprint( dict(events_hist) )

    return event_samples


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
    event_samples = extract_events_from_samples(samples_db)

    if verbose:
        print("INFO: All the event-based samples:")
        for event in event_samples:
            pprint.pprint(event)
            print("----------------")
    print( "INFO: There are {} event-based samples.".format(len(event_samples)) )

if __name__ == "__main__":
    main()
