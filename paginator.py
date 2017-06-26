import os
import ceilomarius
from datetime import datetime, timedelta
import argparse

class Paginator:
    def __init__(self, endpoint, token):
        ceilo = ceilomarius.Ceilomarius(api_version = 2,
                            endpoint = endpoint,
                            token = token,
                            verbose = False)
        self.ceilo = ceilo

    def convert_date(self, date):
        return "{:%Y-%m-%dT%H:%M:%S.%f}".format(date)

    def get_meters_for_instance(self, instance_id, time_begin, time_end, limit = 100):
        time_latest = time_end
        print( "INFO: Latest timestamp on the page: {}".format(self.convert_date(time_latest)) )
        query = [{"field": "resource_id", "op": "eq", "value": instance_id}, {"field": "timestamp", "op": "gt", "value": self.convert_date(time_begin)}, {"field": "timestamp", "op": "le", "value": self.convert_date(time_latest)}]
        return self.ceilo.get_metric(meter_name="instance", q=query, limit=limit).json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_id", help="The name of the instance to fetch meters for.")
    args = parser.parse_args()

    instance_id = args.instance_id

    pag = Paginator(endpoint = os.environ['OS_CEILOMETER_URL'],
                    token = os.environ['OS_TOKEN'])

    t_end = datetime.now()
    t_begin = t_end - timedelta(days=10)
    print("INFO: Retrieving objects from {} to {}".format(pag.convert_date(t_begin), pag.convert_date(t_end)))

    objects = pag.get_meters_for_instance(instance_id, t_begin, t_end)
    print("INFO: Retrieved {} objects.".format(len(objects)))

if __name__ == "__main__":
    main()
