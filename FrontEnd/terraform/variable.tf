#AZURE
variable "resource_group_name" {
  default = "Use the same resource group name used in datagen"
} 

variable "acrname" {
  default = "azure container registry name"
} 

variable "dockertag-frontend" {
  default = "frontend:latest"
} 

variable "webapp_name" {
  default = "provide a name to your webapp"
}

variable "service_principal" {
  default = "webapp service principal name"
}