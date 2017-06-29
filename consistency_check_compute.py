import paginator
import mongor
from datetime import datetime, timedelta
import argparse
import credentials
import config

def compare_samples(samples_api, samples_db):
    print( "INFO: Number of samples from API: {}".format(len(samples_api)) )
    print( "INFO: Number of samples from the database: {}".format(len(samples_db)) )

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

    compare_samples(samples_api, samples_db)

if __name__ == "__main__":
    main()
