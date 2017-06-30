import config
import pymongo
import argparse
from datetime import datetime, timedelta

class Mongor:
    def __init__(self):
        self.conf = config.Config()
        self.client = pymongo.MongoClient(host = self.conf.host, port = int(self.conf.port))

    def get_samples_for_instance(self, instance_id, time_begin, time_end, batch_size=100):
        collection_name="meter"
        db = self.client[self.conf.database]
        db.authenticate(name=self.conf.username, password=self.conf.password, source=self.conf.database)
        cursor = db[collection_name].find({"counter_name": "instance",
                                            "resource_id": instance_id,
                                            "timestamp":
                                                { "$gte": time_begin,
                                                    "$lt": time_end }
                                        }).batch_size(batch_size).sort('timestamp', pymongo.DESCENDING)
        return [c for c in cursor]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_id", help="The name of the instance to fetch samples for.")
    args = parser.parse_args()

    instance_id = args.instance_id

    mongor = Mongor()

    t_end = datetime.utcnow()
    t_begin = t_end - timedelta(days=10)
    print("INFO: Retrieving objects from {} to {}".format(t_begin, t_end))
    samples = mongor.get_samples_for_instance(instance_id, t_begin, t_end)
    print("INFO: Retrieved {} samples.".format( len(samples) ) )
    print("INFO: The first sample:")
    print( samples[-1] )
    print("INFO: The last sample:")
    print( samples[0] )

if __name__ == "__main__":
    main()
