output "resource_group" {
  value = azurerm_resource_group.main.name
}

output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

output "key_vault_name" {
  value = azurerm_key_vault.main.name
}

output "identity_client_id" {
  value = azurerm_user_assigned_identity.app.client_id
}

output "identity_id" {
  value = azurerm_user_assigned_identity.app.id
}

output "openai_endpoint" {
  value = data.azurerm_cognitive_account.openai.endpoint
}

output "app_url" {
  value = "https://${azurerm_container_app.main.ingress[0].fqdn}"
}
