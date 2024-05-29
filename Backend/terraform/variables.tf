#AZURE
variable "resource_group_name" {
  default = "confluent-genai-azure"
} 

variable "acrname" {
  default = "azuregenaiazurez"
} 

variable "dockertag-backend" {
  default = "backendenv:latest"
} 

variable "service_principal" {
  default = "containerappz"
}

variable "containerapp_name" {
 default = "confluent-genai-azurez" 
}