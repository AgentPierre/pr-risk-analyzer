terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource group — logical container for all resources
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# Key Vault — stores secrets like GitHub PAT and Claude API key
resource "azurerm_key_vault" "main" {
  name                = var.key_vault_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = var.tenant_id
  sku_name            = "standard"
}

# Grant Service Principal access to read Key Vault secrets
resource "azurerm_key_vault_access_policy" "sp_policy" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = var.tenant_id
  object_id    = "90cda166-5d69-47d9-bf0c-bc7e05f86ff5"

  secret_permissions = [
    "Get",
    "List"
  ]
}

# Log Analytics Workspace — persists container logs after exit
resource "azurerm_log_analytics_workspace" "main" {
  name                = "pr-analyzer-logs"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# Read secrets from Key Vault at deploy time
data "azurerm_key_vault_secret" "anthropic_key" {
  name         = "anthropic-api-key"
  key_vault_id = azurerm_key_vault.main.id
}

data "azurerm_key_vault_secret" "github_token" {
  name         = "github-token"
  key_vault_id = azurerm_key_vault.main.id
}

# Container group — runs the analyzer tool
resource "azurerm_container_group" "analyzer" {
  name                = "pr-risk-analyzer"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  ip_address_type     = "None"
  restart_policy      = "Never"

  image_registry_credential {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }

  diagnostics {
    log_analytics {
      workspace_id  = azurerm_log_analytics_workspace.main.workspace_id
      workspace_key = azurerm_log_analytics_workspace.main.primary_shared_key
    }
  }

  container {
    name   = "analyzer"
    image  = "${azurerm_container_registry.acr.login_server}/pr-risk-analyzer:v1"
    cpu    = 0.5
    memory = 1.5

    commands = ["python", "analyze.py", "--repo", "kubernetes/kubernetes", "--limit", "5"]

    secure_environment_variables = {
      ANTHROPIC_API_KEY = data.azurerm_key_vault_secret.anthropic_key.value
      GITHUB_TOKEN      = data.azurerm_key_vault_secret.github_token.value
    }
  }
}

# Azure Container Registry — stores the Docker image
resource "azurerm_container_registry" "acr" {
  name                = "pranalyzeracr"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = true
}

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  default     = "pr-risk-analyzer-rg"
}

variable "location" {
  description = "Azure region to deploy resources"
  default     = "East US"
}

variable "key_vault_name" {
  description = "Name of the Azure Key Vault"
  default     = "pr-analyzer-vault"
}

variable "tenant_id" {
  description = "Azure tenant ID for Key Vault access"
}
