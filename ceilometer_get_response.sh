#!/bin/bash

if [ "$#" -lt 2 ];
then
    echo "Usage: $0 <token_id> <instance_id>"
    exit 1;
fi

set -x

OS_TOKEN=$1
if [ -z $OS_CEILOMETER_URL ];
then
    OS_CEILOMETER_URL=https://compute.datacentred.io:8777
    echo "WARNING: '$OS_CEILOMETER_URL' not set, setting it to $OS_CEILOMETER_URL"
fi

INSTANCE_ID=$2

curl -s -H "X-Auth-Token: $OS_TOKEN" \
    -X GET \
    -H "Content-Type: application/json" \
    $OS_CEILOMETER_URL/v2/events \
    -d '{ "q": [{"field": "instance_id", "op": "eq", "value": "'$INSTANCE_ID'"}], "limit": 1 }' \
    | python -m json.tool
    #-d '{ "q": [{"field": "timestamp", "op": "ge", "value": "2017-06-01T00:00:00"}, {"field": "timestamp", "op": "lt", "value": "2017-06-01T00:10:00"}], "limit": 1 }' \
echo

curl -s -H "X-Auth-Token: $OS_TOKEN" \
    -X GET \
    -H "Content-Type: application/json" \
    $OS_CEILOMETER_URL/v2/meters/instance \
    -d '{ "q": [{"field": "resource_id", "op": "eq", "value": "'$INSTANCE_ID'"}, {"field": "metadata.event_type", "op": "eq", "value": "compute.instance.exists"}], "limit": 1 }' \
    | python -m json.tool
    #-d '{ "q": [{"field": "timestamp", "op": "ge", "value": "2017-06-01T00:00:00"}, {"field": "timestamp", "op": "lt", "value": "2017-06-01T00:10:00"}], "limit": 1 }' \
echo

curl -s -H "X-Auth-Token: $OS_TOKEN" \
    -X GET \
    -H "Content-Type: application/json" \
    $OS_CEILOMETER_URL/v2/samples \
    -d '{ "q": [{"field": "resource_id", "op": "eq", "value": "'$INSTANCE_ID'"}, {"field": "meter", "op": "eq", "value": "instance"}], "limit": 1 }' \
    | python -m json.tool
    #-d '{ "q": [{"field": "timestamp", "op": "ge", "value": "2017-06-01T00:00:00"}, {"field": "timestamp", "op": "lt", "value": "2017-06-01T01:00:00"}] }' \
echo

set +x
