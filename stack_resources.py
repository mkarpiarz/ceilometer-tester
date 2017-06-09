import os
import credentials
import heatclient.client

def main():
    if not os.environ.get('OS_HEAT_URL'):
        print("ERROR: $OS_HEAT_URL variable not set!")
        print("Use this as an example: OS_HEAT_URL=https://compute.datacentred.io:8004/v1/`echo $OS_PROJECT_ID`")
        exit(1)

    # get a token
    creds = credentials.Credentials()
    token = creds.get_token()

    heat = heatclient.client.Client(1,
                            endpoint=os.environ['OS_HEAT_URL'],
                            token=token)

    stacks = heat.stacks.list()
    for stack in stacks:
        print stack
        print( heat.resources.list(stack_id = stack.id) )

if __name__ == "__main__":
    main()
