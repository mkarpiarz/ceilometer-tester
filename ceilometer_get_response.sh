#!/bin/bash

if [ "$#" -eq 0 ];
then
    echo "Usage: $0 <token_id>"
    exit 1;
fi

set -x

OS_TOKEN=$1
OS_CEILOMETER_URL=https://compute.datacentred.io:8777
if [ -z $OS_PROJECT_ID ];
then
    echo "ERROR: Variable $OS_PROJECT_ID not set!"
    exit 2
fi

curl -s -H "X-Auth-Token: $OS_TOKEN" \
    -X GET \
    -H "Content-Type: application/json" \
    $OS_CEILOMETER_URL/v2/meters/instance \
    -d '{ "q": [{"field": "project_id", "op": "eq", "value": "'$OS_PROJECT_ID'"}, {"field": "metadata.event_type", "op": "eq", "value": "compute.instance.exists"}], "limit": 1 }' \
    | python -m json.tool
    #-d '{ "q": [{"field": "timestamp", "op": "ge", "value": "2017-06-01T00:00:00"}, {"field": "timestamp", "op": "lt", "value": "2017-06-01T00:10:00"}], "limit": 1 }' \
echo

curl -s -H "X-Auth-Token: $OS_TOKEN" \
    -X GET \
    -H "Content-Type: application/json" \
    -d '{ "q": [{"field": "project_id", "op": "eq", "value": "'$OS_PROJECT_ID'"}, {"field": "meter", "op": "eq", "value": "instance"}], "limit": 1 }' \
    $OS_CEILOMETER_URL/v2/samples \
    | python -m json.tool
    #-d '{ "q": [{"field": "timestamp", "op": "ge", "value": "2017-06-01T00:00:00"}, {"field": "timestamp", "op": "lt", "value": "2017-06-01T01:00:00"}] }' \
echo

set +x
