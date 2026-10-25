using System;
using D365.Plugins.Common;
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Query;

namespace D365.Plugins.Contact
{
    /// <summary>
    /// Blocks a Contact whose primary email (emailaddress1) is already used by another active Contact.
    /// The lookup runs as SYSTEM so duplicates owned by other users are found too.
    ///
    /// Register:
    ///   Message: Create | Table: contact | Stage: PreValidation (10) | Mode: Synchronous
    ///   Message: Update | Table: contact | Stage: PreValidation (10) | Mode: Synchronous
    ///                     Filtering attributes: emailaddress1
    ///
    /// Note: two saves at the same instant can both pass this check. For a hard guarantee,
    /// add an alternate key on emailaddress1 as well (covered in the book's duplicate-prevention chapter).
    /// </summary>
    public class ContactDuplicateEmailPlugin : PluginBase
    {
        private const string EmailAttribute = "emailaddress1";

        protected override void ExecutePlugin(LocalPluginContext localContext)
        {
            var context = localContext.PluginExecutionContext;
            if (context.PrimaryEntityName != "contact" || context.Stage != PipelineStage.PreValidation)
            {
                localContext.Trace("Registered on an unexpected step; nothing to do.");
                return;
            }

            var target = localContext.GetTargetEntity();
            if (target == null || !target.Contains(EmailAttribute))
            {
                return;
            }

            var email = target.GetAttributeValue<string>(EmailAttribute);
            if (string.IsNullOrWhiteSpace(email))
            {
                return;
            }

            email = email.Trim();

            var query = new QueryExpression("contact")
            {
                ColumnSet = new ColumnSet("fullname"),
                TopCount = 1,
                NoLock = true
            };
            query.Criteria.AddCondition(EmailAttribute, ConditionOperator.Equal, email);
            query.Criteria.AddCondition("statecode", ConditionOperator.Equal, 0);

            // On Update, ignore the record being saved.
            if (context.MessageName == "Update" && target.Id != Guid.Empty)
            {
                query.Criteria.AddCondition("contactid", ConditionOperator.NotEqual, target.Id);
            }

            var matches = localContext.SystemOrganizationService.RetrieveMultiple(query);
            if (matches.Entities.Count > 0)
            {
                var existingName = matches.Entities[0].GetAttributeValue<string>("fullname");
                throw new InvalidPluginExecutionException(
                    string.Format("A contact with the email {0} already exists ({1}). Open that contact instead of creating a duplicate.", email, existingName));
            }

            localContext.Trace("No active contact uses {0}.", email);
        }
    }
}
