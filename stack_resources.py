import os
import credentials
import heatclient.client
import resource

class Heat:
    def __init__(self):
        if not os.environ.get('OS_HEAT_URL'):
            print("ERROR: $OS_HEAT_URL variable not set!")
            print("Use this as an example: OS_HEAT_URL=https://compute.datacentred.io:8004/v1/`echo $OS_PROJECT_ID`")
            exit(1)

        # get a token
        creds = credentials.Credentials()
        token = creds.get_token()

        self.heat = heatclient.client.Client(1,
                                            endpoint=os.environ['OS_HEAT_URL'],
                                            token=token)

    def get_stacks(self):
        return self.heat.stacks.list()

    def get_resources_in_stack(self, stack_id):
        # original resources from the stack
        stack_resources = self.heat.resources.list(stack_id = stack_id)
        # a list of simpler Resource objects
        resources = [ resource.Resource(res.physical_resource_id, res.resource_type) for res in stack_resources ]
        #return self.heat.resources.list(stack_id = stack_id)
        return resources

def main():
    heat = Heat()
    stacks = heat.get_stacks()
    for stack in stacks:
        print( stack )
        resources = heat.get_resources_in_stack(stack.id)
        for res in resources:
            print res

if __name__ == "__main__":
    main()
