#!/bin/bash

if [ "$#" -lt 2 ];
then
    echo "Usage: $0 <token_id> <instance_id>"
    exit 1;
fi

send_request() {
    # $1: url
    # $2: token
    # $3: query
    set -x
    curl -s -H "X-Auth-Token: $2" \
        -X GET \
        -H "Content-Type: application/json" \
        $1 \
        -d "$3" \
        | python -m json.tool
    set +x
}

OS_TOKEN=$1
if [ -z $OS_CEILOMETER_URL ];
then
    OS_CEILOMETER_URL=https://compute.datacentred.io:8777
    echo "WARNING: '$OS_CEILOMETER_URL' not set, setting it to $OS_CEILOMETER_URL"
fi
INSTANCE_ID=$2

# Get an event
url=$OS_CEILOMETER_URL/v2/events
query='{ "q": [{"field": "instance_id", "op": "eq", "value": "'$INSTANCE_ID'"}], "limit": 1 }'
send_request $url $OS_TOKEN "$query"

# Get a sample
url=$OS_CEILOMETER_URL/v2/meters/instance
query='{ "q": [{"field": "resource_id", "op": "eq", "value": "'$INSTANCE_ID'"}, {"field": "metadata.event_type", "op": "eq", "value": "compute.instance.exists"}], "limit": 1 }'
send_request $url $OS_TOKEN "$query"

# Get a sample with a different endpoint
url=$OS_CEILOMETER_URL/v2/samples
query='{ "q": [{"field": "resource_id", "op": "eq", "value": "'$INSTANCE_ID'"}, {"field": "meter", "op": "eq", "value": "instance"}], "limit": 1 }' \
send_request $url $OS_TOKEN "$query"
