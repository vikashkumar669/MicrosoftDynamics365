# D365.Plugins

Dataverse / Dynamics 365 plugins used in the training book *Microsoft Dynamics 365 & Dataverse Plugin Development*. One assembly, one class per plugin, all sharing `PluginBase`.

- Target: .NET Framework 4.8 (Dataverse supports 4.6.2–4.8)
- SDK: `Microsoft.CrmSdk.CoreAssemblies` (Microsoft.Xrm.Sdk), restored from NuGet
- Signed with `D365.Plugins.snk` (required for a classic plugin assembly)
- Build: open `D365.Plugins.sln` in Visual Studio 2022/2026 and build, or run `dotnet build -c Release`
- Output: `src/D365.Plugins/bin/Release/net48/D365.Plugins.dll` — register only this DLL, never `Microsoft.Xrm.Sdk.dll`

## Plugins and their registration

| Plugin | Table | Message | Stage | Mode | Filtering attributes / images / config |
| --- | --- | --- | --- | --- | --- |
| `AccountNumberValidationPlugin` | account | Create | PreValidation (10) | Sync | — |
| `AccountNumberValidationPlugin` | account | Update | PreValidation (10) | Sync | accountnumber |
| `AccountFollowUpTaskPlugin` | account | Create | PostOperation (40) | Sync | — |
| `ContactDefaultsPlugin` | contact | Create | PreOperation (20) | Sync | — |
| `ContactDefaultsPlugin` | contact | Update | PreOperation (20) | Sync | firstname, lastname |
| `ContactDuplicateEmailPlugin` | contact | Create | PreValidation (10) | Sync | — |
| `ContactDuplicateEmailPlugin` | contact | Update | PreValidation (10) | Sync | emailaddress1 |
| `CasePriorityPlugin` | incident | Create | PreOperation (20) | Sync | Unsecure config (optional): `urgent,outage,down,critical` |
| `ContextTracePlugin` | account | Update | PostOperation (40) | Async | Pre image `PreImage` and post image `PostImage` (name, accountnumber) |

## What each plugin does

- **AccountNumberValidationPlugin** — rejects an account whose Account Number is empty or not `ACC-12345`.
- **AccountFollowUpTaskPlugin** — creates a "Welcome call" task regarding a new account, due in 7 days.
- **ContactDefaultsPlugin** — trims names and, on create, defaults Preferred Method of Contact to Email when an email is given.
- **ContactDuplicateEmailPlugin** — blocks a second active contact with the same primary email (lookup runs as SYSTEM).
- **CasePriorityPlugin** — Customer Service: sets a new case's priority to High when its title contains a keyword.
- **ContextTracePlugin** — writes the full execution context (parameters, images, depth, users) to the Plug-in Trace Log.

## Register with the Plug-in Registration Tool

1. Install the Power Platform CLI, then run `pac tool prt` to install and open the tool.
2. **Create New Connection** → Office 365 → sign in to your environment.
3. **Register → Register New Assembly** → select `D365.Plugins.dll` → Isolation mode **Sandbox**, location **Database** → **Register Selected Plugins**.
4. For each row in the table above: right-click the plugin type → **Register New Step**, set message, primary entity, stage, mode and filtering attributes → **Register New Step**.
5. For `ContextTracePlugin`: right-click its step → **Register New Image**, add `PreImage` and `PostImage`.
6. Turn on tracing: in the app, **Settings (gear) → Advanced settings → Settings → Administration → System Settings → Customization tab → Enable logging to plug-in trace log = All**. Switch it back to Exception or Off after testing, because trace logs use storage.

## Quick tests

| Test | Expected result |
| --- | --- |
| Create an account with Account Number `12345` | Error: "Account Number '12345' is not valid…" |
| Create an account with Account Number `ACC-00001` | Saved; a "Welcome call" task appears under Activities |
| Create a contact with First Name `  John  ` and an email | Saved as `John`; Preferred Method of Contact = Email |
| Create a second contact with the same email | Error: "A contact with the email … already exists" |
| Create a case titled `Website outage` with no priority | Priority = High |
| Update an account's name | A trace log row shows the full context and both images |

> Status: written for the training book. Build and register it in your own environment before relying on it; nothing here has been run against a live environment yet.
