---
chapter: 6
part: "Part II — Connecting to Dynamics 365 / Dataverse"
title: "Your First Azure Function Connected to Dataverse"
build-summary: "By the end of this chapter, a function running in Azure reads and writes Dataverse records without a single secret in its configuration."
builds:
  - "A reusable, secret-free Dataverse client built on managed identity"
  - "Validated, strongly typed settings that stop a bad deployment at start-up"
  - "The Harbourline Connect `GET /api/properties` endpoint, deployed to Flex Consumption"
versions: ".NET 10 · Azure Functions 4.x isolated worker · Flex Consumption · Microsoft.PowerPlatform.Dataverse.Client 1.2.27 · Azure.Identity 1.21.0"
---

<!-- DESIGN SAMPLE: an excerpt of Chapter 6 used to approve the page
     design in Phase 3. The full chapter is written in Phase 4. -->

::: objectives
- Explain how a Function App proves its identity to Dataverse without a secret.
- Build a `ServiceClient` that takes its tokens from `DefaultAzureCredential`.
- Register the client once, with settings that are validated at start-up.
- Add a managed identity to Dataverse as an application user with a least-privilege role.
- Tell a configuration fault from a permission fault by its error message.
:::

## The business problem

Harbourline Group (a fictional company) is launching a tenant portal. The portal team needs a list of available properties from Dynamics 365, but the portal must never hold Dataverse credentials. Today the property list is exported to a spreadsheet each morning, so tenants see data that is up to a day old.

The integration team's rule is simple: no secrets in code, no secrets in app settings. If a secret is never created, it can never leak, expire on a Friday night, or be copied into the wrong environment.

## How it works

Three facts make secret-free access work.

A **managed identity** is an identity in Microsoft Entra ID that Azure creates and looks after for one resource. The Function App asks the platform for a token for that identity; you never see a password or certificate. A *system-assigned* identity is created with the Function App and deleted with it.

Dataverse accepts a token from an Entra ID identity in its tenant only when that identity exists in the environment as an **application user** with at least one security role. The role, not the token, decides what the function may read and write.

`DefaultAzureCredential` from the Azure.Identity library tries several credential sources in turn, including environment variables, managed identity, and the developer sign-ins of Visual Studio and the Azure CLI. The same code therefore uses your own sign-in on your laptop and the managed identity in Azure.

## Architecture

![The function never holds a secret: Microsoft Entra ID issues tokens to the Function App's managed identity, and Dataverse trusts that identity as an application user.](figures/ch06/architecture.svg){#fig:arch}

::: {#tbl:components caption="Components in @fig:arch"}
| Component | Role | Authenticates with | Failure path |
| --- | --- | --- | --- |
| Tenant portal | Calls the API | Function key (Chapter 14 adds Entra ID) | 401 if the key is missing |
| Function App | Runs Harbourline Connect | System-assigned managed identity | Fails at start-up if settings are invalid |
| Microsoft Entra ID | Issues access tokens | — | Token errors surface as `AuthenticationFailedException` |
| Dataverse | Stores properties | Trusts the identity as an application user | 401/403 without a user or role; 429 when throttled |
| Application Insights | Collects logs and traces | Connection string (Chapter 18 moves to identity) | — |
:::

Data flows left to right. The dashed box is the authentication boundary; the amber arrow is the throttling path that Chapter 15 handles in depth.

## Step-by-step implementation

### Step 1 – Create a Dataverse client that never holds a secret

`ServiceClient` normally takes a connection string. It also has a constructor that takes a *token provider*: a function it calls whenever it needs an access token. @lst:factory passes it a function that asks an Azure `TokenCredential` for one.

```{.csharp #lst:factory include="src/Harbourline.Connect.Core/Dataverse/DataverseClientFactory.cs" region="dataverse-factory" caption="A `ServiceClient` that gets its tokens from an Azure identity"}
```

1. Any `TokenCredential` works. In production it is `DefaultAzureCredential`, which uses `az login` on your laptop and the managed identity in Azure – the same code in both places.
2. The scope is the environment's root URL plus `/.default`: "every permission this identity has been granted on Dataverse".
3. `ServiceClient` calls this function each time it needs a token. Azure.Identity caches tokens, so this is not a network call per request.
4. `useUniqueInstance: true` gives this client its own connection rather than sharing a cached one, which keeps tests and multiple environments independent.

::: security
Nothing in @lst:factory is secret. The environment URL is configuration, not a credential; access is controlled entirely by the security role you give the identity in Step 3.
:::

### Step 2 – Register the client once

Creating a `ServiceClient` is expensive: it authenticates and loads metadata. Register it once, as a singleton, together with validated settings (@lst:registration).

```{.csharp #lst:registration include="src/Harbourline.Connect.Core/ServiceCollectionExtensions.cs" region="dataverse-registration" caption="Registering validated settings and a single Dataverse client"}
```

1. `[Required]` and `[Url]` on `DataverseOptions` are checked, and `ValidateOnStart` makes a missing or malformed `Dataverse__Url` stop the host at start-up instead of failing on the first request.
2. One credential for the whole app. Tests replace it with a substitute.
3. The factory from @lst:factory runs once, the first time a function needs Dataverse.
4. Functions depend on the `IOrganizationServiceAsync2` interface, so Chapter 19 can test them without Dataverse.

::: performance
A singleton `ServiceClient` is safe to share across concurrent invocations. For heavily parallel batch work, Chapter 15 uses `Clone()` to give each worker its own connection.
:::

### Step 3 – Add the managed identity as an application user

The Function App's identity exists in Microsoft Entra ID, but Dataverse ignores it until it is registered as an **application user** with a security role.

::: {.capture #fig:appuser caption="Registering the Function App's managed identity as an application user in Harbourline-Dev." app="Power Platform admin center" path="Environments › Harbourline-Dev › Settings › Users + permissions › Application users › New app user" annotations="1 Add an app; 2 Search box with the identity's application (client) ID; 3 Business unit; 4 Security roles: Harbourline Integration"}
:::

1. Select **New app user**, then **Add an app** ❶.
2. Paste the identity's **application (client) ID** into the search box ❷. Search by ID, not by name: managed identities often do not appear by name.
3. Choose the root business unit ❸.
4. Assign the custom **Harbourline Integration** role ❹, never System Administrator.

**Expected result:** the new application user appears in the list with status **Active**.

::: note
**If your screen differs:** the admin center is updated often. If you don't see **Users + permissions**, open the environment's **Settings** page and search for "Application users".
:::

::: knowledge-check
1. Why does @lst:factory work unchanged on your laptop and in Azure?
2. What happens if `Dataverse__Url` is missing when the Function App starts?
3. Why must you search for the managed identity by application ID?
:::

::: summary
- Use `ServiceClient`'s token-provider constructor with `DefaultAzureCredential`; no secret is ever created.
- Register one `ServiceClient` per app and depend on `IOrganizationServiceAsync2`.
- Validate settings at start-up with `ValidateOnStart` so bad deployments fail fast.
- A managed identity needs an application user and a least-privilege role in each environment.
:::

## References

- [Guide for running C# Azure Functions in the isolated worker model](https://learn.microsoft.com/azure/azure-functions/dotnet-isolated-process-guide) – Microsoft Learn, checked 2026-10-24.
- [Process an equipment request with Azure Functions](https://microsoftlearning.github.io/AB-400-microsoft-power-platform-developer/Instructions/Labs/03-azure-functions-request.html) – Microsoft Learning lab, checked 2026-10-23.
