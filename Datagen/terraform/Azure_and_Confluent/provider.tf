terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "~>1.76.0"
    }
    azurerm = {
        source = "hashicorp/azurerm"
        version = "~>3.105.0"
    }
  }
}
provider "azurerm" {
  skip_provider_registration = "true"
  features {
    resource_group {
prevent_deletion_if_contains_resources = false
}
  }
}
provider "confluent" {
  cloud_api_key    = var.confluent_cloud_api_key
  cloud_api_secret = var.confluent_cloud_api_secret
}