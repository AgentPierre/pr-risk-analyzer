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

# Container group — runs the analyzer tool
resource "azurerm_container_group" "analyzer" {
  name                = "pr-risk-analyzer"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  ip_address_type     = "None"

  container {
    name   = "analyzer"
    image = "mcr.microsoft.com/devcontainers/python:3.11"
    cpu    = "0.5"
    memory = "1.5"

    commands = ["python", "analyze.py", "--repo", "kubernetes/kubernetes", "--limit", "5"]
  }
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
