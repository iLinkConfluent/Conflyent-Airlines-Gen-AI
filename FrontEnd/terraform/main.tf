## Azure Registration

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
# Creating Resource Group
data "azurerm_resource_group" "az_resource_group" {
  name = "${var.resource_group_name}"
}

# Creating Container Registry

resource "azurerm_container_registry" "acr" {
  name                = "${var.acrname}"
  resource_group_name = data.azurerm_resource_group.az_resource_group.name
  location            = data.azurerm_resource_group.az_resource_group.location
  sku                 = "Basic"
  admin_enabled       = true
  public_network_access_enabled = true
}

#Azure container registry login

resource "null_resource" "acrlogin" {
  provisioner "local-exec" {
    command = "az acr login -n ${var.acrname}"
  }
  depends_on = [
   azurerm_container_registry.acr,
   ]
}


# Docker build - Frontend

resource "null_resource" "dockerbuild-frontend" {
  provisioner "local-exec" {
    command = "docker build --platform=linux/amd64 -t ${var.acrname}.azurecr.io/${var.dockertag-frontend} ../"
  }
  depends_on = [
    azurerm_container_registry.acr,
    null_resource.acrlogin,
  ]
}
# Docker push - Frontend 

resource "null_resource" "dockerpush-frontend" {
  provisioner "local-exec" {
    command = "docker push ${var.acrname}.azurecr.io/${var.dockertag-frontend}"
  }
  depends_on = [
    null_resource.dockerbuild-frontend,
    azurerm_container_registry.acr,
    null_resource.acrlogin,
  ]
}

resource "time_sleep" "wait" {
 depends_on = [
    null_resource.dockerbuild-frontend,
    azurerm_container_registry.acr,
    null_resource.acrlogin,
    null_resource.dockerpush-frontend,
  ]

  create_duration = "30s"
}

# Crearing Azure Web App

resource "azurerm_service_plan" "plan" {
  name                = "${var.service_principal}"
  location            = data.azurerm_resource_group.az_resource_group.location
  resource_group_name = data.azurerm_resource_group.az_resource_group.name
  os_type             = "Linux"
  sku_name            = "S1"
   depends_on = [
    resource.time_sleep.wait,
  ]
}

resource "azurerm_linux_web_app" "webapp" {
  name                = "${var.webapp_name}"
  location            = data.azurerm_resource_group.az_resource_group.location
  resource_group_name = data.azurerm_resource_group.az_resource_group.name
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      docker_image_name        = "${var.dockertag-frontend}"
      docker_registry_url      = "https://${var.acrname}.azurecr.io"
      docker_registry_username = azurerm_container_registry.acr.admin_username
      docker_registry_password = azurerm_container_registry.acr.admin_password
    }
  }
  depends_on = [
    resource.time_sleep.wait,
  ]
}