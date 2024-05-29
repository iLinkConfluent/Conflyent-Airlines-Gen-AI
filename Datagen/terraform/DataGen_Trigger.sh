### read output ##
file="./properties.txt"
while IFS='=' read -r key value
do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value}
done < "$file"

echo "bootsStrapServer                     = " ${CONFLUENT_KAFKA_CLUSTER_URL}
echo "confluent_api_secret                 = " ${CONFLUENT_KEY}
echo "confluent_api_key                    = " ${CONFLUENT_SECRET_KEY}
echo "function_app1                        = " ${function_app1}
echo "function_app2                        = " ${function_app2}
echo "function_app3                        = " ${function_app3}
echo "datalake_connection_string           = " ${datalake_connection_string}
echo "CONFLUENT_SCHEMA_REGISTRYURL         = " ${CONFLUENT_SCHEMA_REGISTRYURL}
echo "CONFLUENT_SCHEMA_REGISTRY_AUTH_USER  = " ${CONFLUENT_SCHEMA_REGISTRY_AUTH_USER}

pip3 install -r ../requirements.txt
python3 ../producer_adls.py $datalake_connection_string

postBody='{"conf":{"bootstrap.servers":'${CONFLUENT_KAFKA_CLUSTER_URL}',"security.protocol":"SASL_SSL","sasl.mechanisms":"PLAIN","sasl.username":'${CONFLUENT_KEY}',"sasl.password":'${CONFLUENT_SECRET_KEY}'}, "sr_conf": {"url": '${CONFLUENT_SCHEMA_REGISTRYURL}', "basic.auth.user.info": '${CONFLUENT_SCHEMA_REGISTRY_AUTH_USER}'} }'

curl --location https://${function_app1//\"/}.azurewebsites.net/api/Passenger \
--header 'Content-Type: application/json' \
--data "$postBody"

curl --location https://${function_app2//\"/}.azurewebsites.net/api/FlightItineries \
--header 'Content-Type: application/json' \
--data "$postBody"

curl --location https://${function_app3//\"/}.azurewebsites.net/api/Gate \
--header 'Content-Type: application/json' \
--data "$postBody"