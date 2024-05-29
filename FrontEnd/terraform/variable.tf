#AZURE
variable "resource_group_name" {
  default = "confluent-genai-azure"
} 

variable "acrname" {
  default = "azuregenaiazurez"
} 

variable "dockertag-frontend" {
  default = "frontend:latest"
} 

variable "webapp_name" {
  default = "conflyentazure"
}

variable "service_principal" {
  default = "azurewebappz"
}