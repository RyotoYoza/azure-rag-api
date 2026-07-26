# azure-rag-api
This project is a small FastAPI service exposing a RAG endpoint (Azure OpenAI + a vector store — pgvector on a cheap Postgres flexible server keeps cost down vs. Azure AI Search). 

## Prerequisites

### Azure resource providers

A fresh Azure subscription does not have all resource providers enabled. Register these before running Terraform, or resource creation fails with misleading errors:

```bash
az provider register --namespace Microsoft.Storage
az provider register --namespace Microsoft.ContainerRegistry
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
az provider register --namespace Microsoft.DBforPostgreSQL
az provider register --namespace Microsoft.KeyVault
az provider register --namespace Microsoft.ManagedIdentity
```

Registration is asynchronous and subscription-wide (one-time). Check with:

```bash
az provider list --query "[?registrationState=='Registered'].namespace" -o table
```

### Terraform state backend

Remote state lives in a manually created storage account (`rg-tfstate`), outside Terraform's own lifecycle so `terraform destroy` cannot delete the record of what it built. See `infra/providers.tf` for the backend configuration.

