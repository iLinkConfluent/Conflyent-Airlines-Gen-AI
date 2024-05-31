# Registraing resource provider

# resource "azurerm_resource_provider_registration" "app" {
#   name = "Microsoft.App"
# }
# resource "azurerm_resource_provider_registration" "web" {
#   name = "Microsoft.Web"
# }
# resource "azurerm_resource_provider_registration" "ContainerRegistry" {
#   name = "Microsoft.ContainerRegistry"
# }
# resource "azurerm_resource_provider_registration" "OperationalInsights" {
#   name = "Microsoft.OperationalInsights"
# }

## Creating Resource Group
data "azurerm_resource_group" "az_resource_group" {
  name = "${var.resource_group_name}"
}

## Creating Container Registry

data "azurerm_container_registry" "acr" {
  name                = "${var.acrname}"
  resource_group_name = data.azurerm_resource_group.az_resource_group.name
}

#Azure container registry login

resource "null_resource" "acrlogin" {
  provisioner "local-exec" {
    command = "az acr login -n ${var.acrname}"
  }
  depends_on = [
   data.azurerm_container_registry.acr,
   ]
}

# Docker build - Backend

resource "null_resource" "dockerbuild-backend" {
  provisioner "local-exec" {
    command = "docker build --platform=linux/amd64 -t ${var.acrname}.azurecr.io/${var.dockertag-backend} ../"
  }
   depends_on = [
    data.azurerm_container_registry.acr,
    null_resource.acrlogin,
  ]
}

# Docker push - Backend 

resource "null_resource" "dockerpush-backend" {
  provisioner "local-exec" {
    command = "docker push ${var.acrname}.azurecr.io/${var.dockertag-backend}"
  }
  depends_on = [
    null_resource.dockerbuild-backend,
    data.azurerm_container_registry.acr,
    null_resource.acrlogin,
  ]
}


# Creating Container Apps
resource "azurerm_log_analytics_workspace" "log" {
  name                = "containerappkspacelog1"
  resource_group_name = data.azurerm_resource_group.az_resource_group.name
  location            = data.azurerm_resource_group.az_resource_group.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
  depends_on = [
    null_resource.dockerpush-backend,
    data.azurerm_container_registry.acr,
  ]
}

resource "azurerm_container_app_environment" "env" {
  name                = "containerapviroment1"
  resource_group_name = data.azurerm_resource_group.az_resource_group.name
  location            = data.azurerm_resource_group.az_resource_group.location
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log.id
  depends_on = [
    null_resource.dockerpush-backend,
    data.azurerm_container_registry.acr,
  ]
}

resource "azurerm_container_app" "app" {
  name                         = "${var.containerapp_name}"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name = data.azurerm_resource_group.az_resource_group.name
  revision_mode                = "Single"

  secret {
    name  = "password"
    value = data.azurerm_container_registry.acr.admin_password
  }

  registry {
    server               = "${var.acrname}.azurecr.io"
    username             =  data.azurerm_container_registry.acr.admin_username
    password_secret_name = "password"
  }

  template {
    container {
      name   = "containeraegistry"
      image  = "${var.acrname}.azurecr.io/${var.dockertag-backend}"
      cpu    = 2
      memory = "4Gi"
    }
  }
  depends_on = [
    null_resource.dockerpush-backend,
    data.azurerm_container_registry.acr,
  ]
}
