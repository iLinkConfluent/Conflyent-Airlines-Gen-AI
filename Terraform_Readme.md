# Terraform Execution

By using terraform we are going to perform the following:

* Creation of Azure resources - Resource Group, ADLS blob, Function App, Container Registry, Container App, Azure OpenAI and Web App.
* Creation of Confluent components - Enviroment, Cluster, Topics, Flink and Sink connector.
* Creation of DataGen
* Building Docker images - Frontend and Backend.
* Deploying Docker images to Container App(backend) and Web App(frontend).

## Prerequisites

1. Azure Subscription
2. Confluent Cloud Account
3. Rockset Account
4. Terraform - [Download here](https://developer.hashicorp.com/terraform/install)
5. Azure CLI - [Download here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
6. Docker    - [Download here](https://www.docker.com/products/docker-desktop/)
7. Azure Function CLI - [Download here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp)
8. Python - Make sure you have the latest version of Python installed. If not, [download here](https://www.python.org/downloads/release/python-390/)
9. Git Bash - If not installed, [download here](https://git-scm.com/downloads)
10. Aure Open AI
11. Any code editor

Step1: Clone/Download the source code. Now you will be able to see Three Blocks.

1. DataGen
2. FrontEnd
3. BackEnd

We are going to deploy each blocks in the above order

Step2: Open terminal

Step3: To authenticate with Azure run the below command.

````bash
Az login
````

**Note**: New window will open, kindly enter valid azure login credentials to authenticate

### DataGen

Step1: Navigate to the DataGen folder and open terrform present inside.

Step2: Open `Variable.tf` file and enter the required values.

Step3: Open `Readme_DataGen.md` make sure all the Prerequisites are installed, ifnot install the Prerequisites.

Step4: Run `Create_Components.sh` – to create the azure and confluent components.

Step5: Place the `flight_policy_data.pdf` in the raw folder of the blob container. Refere the Readme Datagen, how to place the pdf.

Step6: Open `properties.txt` which will be created after running `Create_Components.sh`

Step7: Update the `CONFLUENT_SCHEMA_REGISTRYURL` and `CONFLUENT_SCHEMA_REGISTRY_AUTH_USER` vaules. Refer `Readme_DataGen.md` how to create the Schema registry.

Step6: Run `DataGen_Trigger.sh` – to push Data into confluent topics.

Step7: Navigate to the Flink folder present inside the terraform.

Step8: Refere `Readme_DataGen.md` to create flink API key and secret

Step9: Open `Kafka.py` and enter the open ai details.

Step8: open `variabel.tf` file and enter the requried values.

Step9: Run `flink.sh` to execute the flink statements and push data into embeddings topic.

### Rockset

Note: Refere `Readme_DataGen.md`  to create the Rockset intergration for confluent cluster and collection using cofluent topics

### FrontEnd

Step6: Navigate to the FrontEnd folder and open terrform present inside.

Step7: Open `Variable.tf` file and enter the required values. Use the same resource group name used for DataGen.

Step8: Run `Frontend_deploy.sh` – To create azure components and deploy frontend.

### BackEnd

Step9: Navigate to the BackendEnd folder and chat_app present inside.

Step10: Navigate to `client.properties` and update the confluent cluster details.

Step11: Navigate to `config.py` and update the Rockset and OpenAI details.

Step11: Navigate back to the BackEnd folder and open terraform.

Step12: Open `Variable.tf` file and enter the required values. Use the same resource group name used in DataGen.

Step18: Run `Backend_deploy.sh` –To create azure components and deploy Backend.

To destroy the resources created using terraform Navigate to the terraform folder present inside the blocks and run the below command.

````bash
Terraform destroy 
`````

**Note**: terraform destroy will prompt for confirmation
