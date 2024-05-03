### remove residue files
rm -f properties.txt
rm -f ../../Frontend/SocketServer/properties.txt

### Init terraform and do apply
terraform init
terraform validate

if terraform apply --auto-approve; then
    echo "Terraform applied and components created sucessfully"
    terraform output >> properties.txt
    terraform output >> ../../Frontend/SocketServer/properties.txt

file="./properties.txt"
while IFS='=' read -r key value
do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value}
done < "$file"

file="../../Frontend/SocketServer/properties.txt"
while IFS='=' read -r key value
do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value}
done < "$file"

file="../../Frontend/ReactWebApp/properties.txt"
while IFS='=' read -r key value
do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value}
done < "$file"

echo "function_app1              = " ${function_app1}
echo "function_app2              = " ${function_app2}
echo "function_app3              = " ${function_app3}

cd ../Passenger
func azure functionapp publish ${function_app1//\"/} --build-remote 

cd ../FlightItineries
func azure functionapp publish ${function_app2//\"/} --build-remote

cd ../Gate
func azure functionapp publish ${function_app3//\"/} --build-remote

else
    echo "Terraform apply failed, compoments not created"
fi