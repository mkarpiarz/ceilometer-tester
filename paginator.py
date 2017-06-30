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

        # the last timestamp on the list (the oldest)
        time_oldest = time_end

        # aggregate all retrieved samples in this list:
        samples_all = []
        """
        EXPLANATION:
        This procedure fetches a number of samples specified by the `limit` parameter
        from within the specified period, then extracts the timestamp of the oldest
        sample in the batch and sends another query for a "limit" number of samples
        oldest then the one selected previously and repeats until there are no new
        samples. The resulting list includes all the samples from the period.
        This approach prevents creating long running queries that may not end
        before the resulting cursor times out.
        """
        while time_oldest >= time_begin:
            if self.verbose:
                print( "INFO: Oldest timestamp on this page: {}".format(self.convert_date(time_oldest)) )
            query = [{"field": "resource_id", "op": "eq", "value": instance_id},
                        {"field": "timestamp", "op": "ge", "value": self.convert_date(time_begin)},
                        {"field": "timestamp", "op": "lt", "value": self.convert_date(time_oldest)}]
            samples = self.ceilo.get_metric(meter_name="instance", q=query, limit=limit).json()
            # break if there are no more samples
            if not samples:
                break
            # get the oldest timestamp
            sample_oldest = samples[-1]

            time_oldest = self.convert_timestamp( sample_oldest.get('timestamp') )
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
