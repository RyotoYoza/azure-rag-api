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


####Architectural Diagram
Below are the diagram of request path and deployment path
dotted lines = for identity
solid lines  = for dataflow

"Every arrow into a secret-bearing resource is authenticated by managed identity; no credentials exist in the repo, the image, or the running container"

Request Path

```mermaid
flowchart TB
    User([User]) -->|"POST /ask"| CA

    subgraph RG["rg-ragapi-dev — managed by Terraform"]
        CA["Container App<br/>FastAPI · scale-to-zero"]
        PG[("PostgreSQL Flexible Server<br/>pgvector · 1536-dim")]
        KV["Key Vault"]
        AI["Application Insights"]
        MI(["User-Assigned<br/>Managed Identity"])
    end

    subgraph Shared["rg-shared — outside Terraform's lifecycle"]
        AOAI["Azure OpenAI<br/>gpt-5-mini · text-embedding-3-small"]
        ACR["Container Registry"]
    end
    CA -->|"1 · embed question"| AOAI
    CA -->|"2 · top-k cosine search"| PG
    CA -->|"3 · grounded completion"| AOAI
    CA -->|"tokens · cost · latency"| AI

    CA -.->|assumes| MI
    MI -.->|"Key Vault Secrets User"| KV
    MI -.->|"Cognitive Services OpenAI User"| AOAI
    MI -.->|"AcrPull"| ACR

    KV ==>|"DATABASE_URL injected<br/>by the platform"| CA
    ACR ==>|"image pull"| CA
,,,


Deployment path

```mermaid
flowchart TB
    Dev([Developer]) -->|"push branch"| PR["Pull Request"]

    subgraph CI["CI — on pull_request"]
        L["ruff check + format"]
        T["pytest"]
        D["docker build<br/>(no push)"]
        P["terraform plan<br/>posted as PR comment"]
    end

    PR --> L & T & D & P
    L & T & D & P -->|"required status checks"| M{{"Merge to main"}}

    subgraph CD["CD — on push to main"]
        direction TB
        A["azure/login via OIDC<br/>no stored secret"] --> C1["pytest"]
        C1 --> C2["build + push image<br/>tagged with commit SHA"]
        C2 --> C3["terraform apply"]
        C3 --> C4["open DB firewall → ingest KB → close"]
        C4 --> C5["smoke test /health"]
        C5 --> C6["eval gate<br/>17 cases · 85% threshold"]
    end

    M --> A
    C6 -->|"pass"| Live([Live on Azure])
```
