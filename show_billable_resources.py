#!/usr/bin/env python
import os
import ceilometerclient.client

def main():
    if not os.environ.get('OS_CEILOMETER_URL'):
        print("ERROR: $OS_CEILOMETER_URL variable not set!")
        exit(1)

    cclient = ceilometerclient.client.get_client(2,
                               os_username=os.environ['OS_USERNAME'],
                               os_password=os.environ['OS_PASSWORD'],
                               os_tenant_name=os.environ['OS_PROJECT_NAME'],
                               os_auth_url=os.environ['OS_AUTH_URL'],
                               os_endpoint=os.environ['OS_CEILOMETER_URL'],
                               user_domain_id='default',
                               project_domain_id='default')

    print( cclient.samples.list() )
    print( cclient.events.list() )

if __name__ == "__main__":
    main()
