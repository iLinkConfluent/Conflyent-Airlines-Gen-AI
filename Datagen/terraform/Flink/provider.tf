terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "~>1.72.0"
    }
  }
}

provider "confluent" {
  cloud_api_key         = var.confluent_cloud_api_key
  cloud_api_secret      = var.confluent_cloud_api_secret
  organization_id       = var.confluent_organisation_id    
  environment_id        = var.environment_id             #  use CONFLUENT_ENVIRONMENT_ID env var
  flink_compute_pool_id = var.flink_compute_pool_id      #  use FLINK_COMPUTE_POOL_ID env var
  flink_rest_endpoint   = var.flink_rest_endpoint        #  use FLINK_REST_ENDPOINT env var
  flink_api_key         = var.flink_api_key              #  use FLINK_API_KEY env var
  flink_api_secret      = var.flink_api_secret           #  use FLINK_API_SECRET env var
  flink_principal_id    = var.flink_principal_id         
}