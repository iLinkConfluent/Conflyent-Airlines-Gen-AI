#CONFLUENT

variable "confluent_cloud_api_key" {
  default = "confluent cloud api key"
}

variable "confluent_cloud_api_secret" {
 default = "confluent cloud api secret"
}

variable "confluent_service_account" {
  default = "Confluent service account name"
}

variable "confluent_environment_name"{
  default = "confluent enviroment name"
}

variable "confluent_cluster_name"{
  default = "confluent cluster name"
}

variable "flink_display_name" {
  default = "for example flinktest"
}

#AZURE

variable "resource_group_name" {
  default = "Azure resurce group name"
} 

variable "resource_group_location" {
  default = "resource group location"
} 

#BLOB STOGAGE Name's

variable "azure_adls_blob_name"{
  default = "storage account name"
}

variable "azure_functionapp_blob_name1"{
  default = "function app1 storage account name"
}

variable "azure_functionapp_blob_name2"{
  default = "function app2 storage account name"
}

variable "azure_functionapp_blob_name3"{
  default = "function app3 storage account name"
}

#FUNCTION APP Name's

variable "azure_functionapp_Passenger"{
  default = "Azure functionapp1 name"
}

variable "azure_functionapp_FlightItineraries"{
  default = "Azure functionapp2 name"
}

variable "azure_functionapp_Gate"{
  default = "Azure functionapp3 name"
}


