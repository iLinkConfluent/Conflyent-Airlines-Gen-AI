#AZURE
variable "resource_group_name" {
  default = "Use the same resource group name used in datagen"
} 

variable "acrname" {
  default = "Use the same acr name used in frontend"
} 

variable "dockertag-backend" {
  default = "backend:latest"
} 

variable "service_principal" {
  default = "container app service principal name"
}

variable "containerapp_name" {
 default = "provide a name to your containerapp" 
}