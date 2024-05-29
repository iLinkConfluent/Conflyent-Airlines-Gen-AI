# Azure Registration

# resource "azurerm_resource_provider_registration" "app" {
#   name = "microsoft.insights"
# }

# resource "azurerm_resource_provider_registration" "app2" {
#   name = "Microsoft.Storage"
# }

############################# Azure Resource Group #############################
resource "azurerm_resource_group" "az_resource_group" {
  name = "${var.resource_group_name}"
  location = "${var.resource_group_location}"
}

############################# Azure ADLS #############################
resource "azurerm_storage_account" "adlsgen2" {
  name                     = "${var.azure_adls_blob_name}"
  resource_group_name      = azurerm_resource_group.az_resource_group.name
  location                 = azurerm_resource_group.az_resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"
}

resource "azurerm_storage_data_lake_gen2_filesystem" "container" {
  name               = "gen-ai"
  storage_account_id = azurerm_storage_account.adlsgen2.id
}
resource "azurerm_storage_data_lake_gen2_path" "raw" {
  path               = "raw"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.container.name
  storage_account_id = azurerm_storage_account.adlsgen2.id
  resource           = "directory"
}
resource "azurerm_storage_data_lake_gen2_path" "topics" {
  path               = "topics"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.container.name
  storage_account_id = azurerm_storage_account.adlsgen2.id
  resource           = "directory"
}

########################## Azure Function App1 ##################################

resource "azurerm_storage_account" "blob1" {
  name                     = "${var.azure_functionapp_blob_name1}"
  resource_group_name      = azurerm_resource_group.az_resource_group.name
  location                 = azurerm_resource_group.az_resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
resource "azurerm_service_plan" "serviceplan1" {
  name                = "azgenaicnftserviceplan1"
  location            = azurerm_resource_group.az_resource_group.location
  resource_group_name = azurerm_resource_group.az_resource_group.name
  os_type             = "Linux"
  sku_name            = "Y1"
  
}
resource "azurerm_application_insights" "test1" {
  name                = "azgenaicnftinsight1"
  location            = azurerm_resource_group.az_resource_group.location
  resource_group_name = azurerm_resource_group.az_resource_group.name
  application_type    = "web"
}

resource "azurerm_function_app" "app1" {
  name                       = "${var.azure_functionapp_Passenger}"
  location                   = azurerm_resource_group.az_resource_group.location
  resource_group_name        = azurerm_resource_group.az_resource_group.name
  app_service_plan_id        = azurerm_service_plan.serviceplan1.id
  storage_account_name       = azurerm_storage_account.blob1.name
  storage_account_access_key = azurerm_storage_account.blob1.primary_access_key
  os_type                    = "linux"
  version                    = "~4"

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
    APPINSIGHTS_INSTRUMENTATIONKEY     = "${azurerm_application_insights.test1.instrumentation_key}"
  }

  site_config {
    linux_fx_version = "python|3.10"
  }
} 


###################################### Azure Function App2 ###############################


resource "azurerm_storage_account" "blob2" {
  name                     = "${var.azure_functionapp_blob_name2}"
  resource_group_name      = azurerm_resource_group.az_resource_group.name
  location                 = azurerm_resource_group.az_resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
resource "azurerm_service_plan" "serviceplan2" {
  name                = "azgenaicnftserviceplan2"
  location            = azurerm_resource_group.az_resource_group.location
  resource_group_name = azurerm_resource_group.az_resource_group.name
  os_type             = "Linux"
  sku_name            = "Y1"
  
}
resource "azurerm_application_insights" "test2" {
  name                = "azgenaicnftinsight2"
  location            = azurerm_resource_group.az_resource_group.location
  resource_group_name = azurerm_resource_group.az_resource_group.name
  application_type    = "web"
}

resource "azurerm_function_app" "app2" {
  name                       = "${var.azure_functionapp_FlightItineries}"
  location                   = azurerm_resource_group.az_resource_group.location
  resource_group_name        = azurerm_resource_group.az_resource_group.name
  app_service_plan_id        = azurerm_service_plan.serviceplan2.id
  storage_account_name       = azurerm_storage_account.blob2.name
  storage_account_access_key = azurerm_storage_account.blob2.primary_access_key
  os_type                    = "linux"
  version                    = "~4"

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
    APPINSIGHTS_INSTRUMENTATIONKEY     = "${azurerm_application_insights.test2.instrumentation_key}"
  }

  site_config {
    linux_fx_version = "python|3.10"
  }
} 


###################################### Azure Function App3 ###############################


resource "azurerm_storage_account" "blob3" {
  name                     = "${var.azure_functionapp_blob_name3}"
  resource_group_name      = azurerm_resource_group.az_resource_group.name
  location                 = azurerm_resource_group.az_resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
resource "azurerm_service_plan" "serviceplan3" {
  name                = "azgenaicnftserviceplan3"
  location            = azurerm_resource_group.az_resource_group.location
  resource_group_name = azurerm_resource_group.az_resource_group.name
  os_type             = "Linux"
  sku_name            = "Y1"
  
}
resource "azurerm_application_insights" "test3" {
  name                = "azgenaicnftinsight3"
  location            = azurerm_resource_group.az_resource_group.location
  resource_group_name = azurerm_resource_group.az_resource_group.name
  application_type    = "web"
}

resource "azurerm_function_app" "app3" {
  name                       = "${var.azure_functionapp_Gate}"
  location                   = azurerm_resource_group.az_resource_group.location
  resource_group_name        = azurerm_resource_group.az_resource_group.name
  app_service_plan_id        = azurerm_service_plan.serviceplan3.id
  storage_account_name       = azurerm_storage_account.blob3.name
  storage_account_access_key = azurerm_storage_account.blob3.primary_access_key
  os_type                    = "linux"
  version                    = "~4"

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
    APPINSIGHTS_INSTRUMENTATIONKEY     = "${azurerm_application_insights.test3.instrumentation_key}"
  }

  site_config {
    linux_fx_version = "python|3.10"
  }
} 

################################ CONFLUENT #####################################

#creating confluent enviroment
resource "confluent_environment" "staging" {
  display_name = "${var.confluent_environment_name}"
}

#Confluent environment attributes
data "confluent_schema_registry_region" "essentials" {
  cloud   = "AZURE"
  region  = "westus2"
  package = "ESSENTIALS"
}

resource "confluent_schema_registry_cluster" "essentials" {
  package = data.confluent_schema_registry_region.essentials.package
  environment {
    id = confluent_environment.staging.id
  }
  region {
    id = data.confluent_schema_registry_region.essentials.id
  }
}

# creating confluent cluster
resource "confluent_kafka_cluster" "standard" {
  display_name = "${var.confluent_cluster_name}"
  availability = "SINGLE_ZONE"
  cloud        = "AZURE"
  region       = "eastus"
  standard {}
  environment {
    id = confluent_environment.staging.id
  }
}

# creating service account and associate with cluster
resource "confluent_service_account" "app-manager" {
  display_name = "${var.confluent_service_account}"
  description  = "Service account to manage Kafka cluster"
}

resource "confluent_role_binding" "app-manager-kafka-cluster-admin" {
  principal   = "User:${confluent_service_account.app-manager.id}"
  role_name   = "CloudClusterAdmin"
  crn_pattern = confluent_kafka_cluster.standard.rbac_crn
}


#################### configuring Kafka API keys #####################

resource "confluent_api_key" "app-manager-kafka-api-key" {
  display_name = "app-manager-kafka-api-key"
  description  = "Kafka API Key that is owned by 'app-manager' service account"
  owner {
    id          = confluent_service_account.app-manager.id
    api_version = confluent_service_account.app-manager.api_version
    kind        = confluent_service_account.app-manager.kind
  }
  managed_resource {
    id          = confluent_kafka_cluster.standard.id
    api_version = confluent_kafka_cluster.standard.api_version
    kind        = confluent_kafka_cluster.standard.kind
    environment {
      id = confluent_environment.staging.id
    }
  }
  depends_on = [
    confluent_role_binding.app-manager-kafka-cluster-admin
  ]
}

#################### createing kafka topics  #########################
resource "confluent_kafka_topic" "FlightPolicyData" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = "FlightPolicyData"
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  partitions_count = 1
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}
resource "confluent_kafka_topic" "FlightItineriesData" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = "FlightItineriesData"
  partitions_count = 1
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_kafka_topic" "FlightGateData" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = "FlightGateData"
  partitions_count = 1
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_kafka_topic" "FlightCustomerData" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = "FlightCustomerData"
  partitions_count = 1
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_kafka_topic" "Questions" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = "Questions"
  partitions_count = 1
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_kafka_topic" "Answers" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = "Answers"
  partitions_count = 1
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_kafka_topic" "FlightDataConsolidatedEmbeddings" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  topic_name    = "FlightDataConsolidatedEmbeddings"
  partitions_count = 1
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

############################ KAFKA ACL ################################
resource "confluent_kafka_acl" "read-write-on-topics" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  resource_type = "TOPIC"
  resource_name = "*"
  pattern_type  = "LITERAL"
  principal     = "User:${confluent_service_account.app-manager.id}"
  host          = "*"
  operation     = "ALL"
  permission    = "ALLOW"
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_kafka_acl" "app-cluster-describe" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  resource_type = "CLUSTER"
  resource_name = "kafka-cluster"
  pattern_type  = "LITERAL"
  principal     = "User:${confluent_service_account.app-manager.id}"
  host          = "*"
  operation     = "DESCRIBE"
  permission    = "ALLOW"
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}

resource "confluent_kafka_acl" "read-write-on-group" {
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  resource_type = "GROUP"
  resource_name = "*"
  pattern_type  = "LITERAL"
  principal     = "User:${confluent_service_account.app-manager.id}"
  host          = "*"
  operation     = "ALL"
  permission    = "ALLOW"
  rest_endpoint = confluent_kafka_cluster.standard.rest_endpoint
  credentials {
    key    = confluent_api_key.app-manager-kafka-api-key.id
    secret = confluent_api_key.app-manager-kafka-api-key.secret
  }
}


resource "confluent_connector" "Azureadlssink" {
  environment {
    id = confluent_environment.staging.id
  }
  kafka_cluster {
    id = confluent_kafka_cluster.standard.id
  }
  config_sensitive = {
  "azblob.account.key" = azurerm_storage_account.adlsgen2.primary_access_key,
  }
  
  config_nonsensitive = {

  "connector.class"             =  "AzureBlobSource",
  "name"                        =  "adlsgenai-genai-blob",
  "topic.regex.list"            =  "FlightPolicyData:.*",
  "kafka.auth.mode"             =  "SERVICE_ACCOUNT",
  "kafka.service.account.id"    =  confluent_service_account.app-manager.id,
  "azblob.account.name"         =  azurerm_storage_account.adlsgen2.name,
  
  "azblob.container.name"       =  azurerm_storage_data_lake_gen2_filesystem.container.name,
  "input.data.format"           =  "BYTES",
  "tasks.max"                   =  "1",
}


  depends_on = [
    azurerm_storage_account.adlsgen2,
    confluent_kafka_acl.app-cluster-describe,
    confluent_kafka_acl.read-write-on-topics,
  ]
}

####################flink#############################

resource "confluent_flink_compute_pool" "main" {
  display_name     = var.flink_display_name
  cloud        = "AZURE"
  region       = "eastus"
  max_cfu          = 5
  environment {
    id = confluent_environment.staging.id
    }
}


############################## terraform output ################################
 
output "CONFLUENT_KAFKA_CLUSTER_URL" {
  description = "Bootstrap endpoint of kafka cluster"
  value       = confluent_kafka_cluster.standard.bootstrap_endpoint
}

output "CONFLUENT_SECRET_KEY"{
  description = "Confluent api secret"
  value = nonsensitive(confluent_api_key.app-manager-kafka-api-key.secret)
}

output "CONFLUENT_KEY" {
  description = "Confluent api key"
  value = confluent_api_key.app-manager-kafka-api-key.id
}

output "saslMechanisms" {
  value = "PLAIN"
}

output "securityProtocol" {
  value = "SASL_SSL"
}

output "function_app1" {
  description = "Function App 1"
  value = azurerm_function_app.app1.name
}

output "function_app2" {
  description = "Function App 2"
  value = azurerm_function_app.app2.name
}

output "function_app3" {
  description = "Function App 3"
  value = azurerm_function_app.app3.name
}

output "datalake_connection_string" {
  description = "gen2 data lake connection string"
  value = nonsensitive(azurerm_storage_account.adlsgen2.primary_connection_string)
  sensitive = false
}

output "CONFLUENT_SCHEMA_REGISTRYURL" {
  value = "***"
}

output "CONFLUENT_SCHEMA_REGISTRY_AUTH_USER" {
  value = "***"
}
###################################################################################