using System;
using D365.Plugins.Common;
using Microsoft.Xrm.Sdk;

namespace D365.Plugins.Account
{
    /// <summary>
    /// After an Account is created, creates a follow-up Task regarding it, due in 7 days.
    /// Runs in PostOperation so the Account ID exists; synchronous, so if the Task can't be
    /// created the whole operation (Account included) rolls back.
    ///
    /// Register:
    ///   Message: Create | Table: account | Stage: PostOperation (40) | Mode: Synchronous
    /// </summary>
    public class AccountFollowUpTaskPlugin : PluginBase
    {
        private const int FollowUpDays = 7;

        protected override void ExecutePlugin(LocalPluginContext localContext)
        {
            var context = localContext.PluginExecutionContext;
            if (!localContext.IsStep("account", "Create", PipelineStage.PostOperation))
            {
                localContext.Trace("Registered on an unexpected step; nothing to do.");
                return;
            }

            var accountId = context.PrimaryEntityId;
            if (accountId == Guid.Empty && context.OutputParameters.Contains("id"))
            {
                accountId = (Guid)context.OutputParameters["id"];
            }

            var target = localContext.GetTargetEntity();
            var accountName = target != null ? target.GetAttributeValue<string>("name") : null;

            var task = new Entity("task");
            task["subject"] = string.Format("Welcome call: {0}", string.IsNullOrWhiteSpace(accountName) ? "new account" : accountName);
            task["description"] = "Created automatically by AccountFollowUpTaskPlugin when the account was created.";
            task["regardingobjectid"] = new EntityReference("account", accountId);
            task["scheduledend"] = DateTime.UtcNow.AddDays(FollowUpDays);

            var taskId = localContext.OrganizationService.Create(task);
            localContext.Trace("Created follow-up task {0} for account {1}.", taskId, accountId);
        }
    }
}
