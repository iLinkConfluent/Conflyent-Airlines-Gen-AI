#CONFLUENT
variable "confluent_cloud_api_key" {
  default = "XXX"
}

variable "confluent_cloud_api_secret" {
 default = "XXX"
}

variable "confluent_organisation_id" {
  default = "XXX"
}

variable "environment_id" {
  default = "conluent enviroment id"
}

variable "flink_compute_pool_id"{
  default = "for example flinktest"
}

variable "flink_rest_endpoint"{
  default = "https://flink.{cloud region}.{cloud provider}.confluent.cloud"
}

variable "flink_api_key" {
  default = "flink api key"
}

variable "flink_api_secret"{
  default = "flink api secret"
}

variable "flink_principal_id"{
  default = "flink account id"
}
variable "confluent_environment_display_name"{
  default = "confluent enviroment name"
}

variable "confluent_kafka_cluster_display_name"{
  default = "confluent cluster name"
}