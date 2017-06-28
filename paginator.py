import os
import ceilomarius
from datetime import datetime, timedelta
import argparse

class Paginator:
    def __init__(self, endpoint, token, verbose = False):
        ceilo = ceilomarius.Ceilomarius(api_version = 2,
                            endpoint = endpoint,
                            token = token,
                            verbose = verbose)
        self.verbose = verbose
        self.ceilo = ceilo

    def convert_date(self, date):
        return "{:%Y-%m-%dT%H:%M:%S.%f}".format(date)

    def convert_timestamp(self, timestamp):
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")

    def get_samples_for_instance(self, instance_id, time_begin, time_end, limit = 100):
        """Returns samples for specified instance divided into pages.

        Attributes:
        limit -- specifies the number of results on a page
        """
        # TODO: Make sure returned results are sorted by timestamps as expected
        # and there is nothing missing missing between pages.

        # the last timestamp on the list (the earliest)
        time_earliest = time_end

        # aggregate all retrieved samples in this list:
        samples_all = []
        while time_earliest >= time_begin:
            if self.verbose:
                print( "INFO: Latest timestamp on the page: {}".format(self.convert_date(time_earliest)) )
            query = [{"field": "resource_id", "op": "eq", "value": instance_id}, {"field": "timestamp", "op": "ge", "value": self.convert_date(time_begin)}, {"field": "timestamp", "op": "lt", "value": self.convert_date(time_earliest)}]
            #print( self.ceilo.get_statistics(meter_name="instance", q=query, count_only=True).json() )
            samples = self.ceilo.get_metric(meter_name="instance", q=query, limit=limit).json()
            # break if there are no more samples
            if not samples:
                break
            # get the earliest timestamp
            sample_earliest = samples[-1]

            time_earliest = self.convert_timestamp( sample_earliest.get('timestamp') )
            # now append samples from this page to the total list
            samples_all += samples

        return samples_all


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_id", help="The name of the instance to fetch samples for.")
    args = parser.parse_args()

    instance_id = args.instance_id

    pag = Paginator(endpoint = os.environ['OS_CEILOMETER_URL'],
                    token = os.environ['OS_TOKEN'],
                    verbose = True)

    t_end = datetime.utcnow()
    t_begin = t_end - timedelta(days=10)
    print("INFO: Retrieving samples from {} to {}".format(pag.convert_date(t_begin), pag.convert_date(t_end)))

    samples = pag.get_samples_for_instance(instance_id, t_begin, t_end)
    if samples:
        print("INFO: Retrieved {} samples.".format(len(samples)))

if __name__ == "__main__":
    main()
