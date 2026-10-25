using System.Text.RegularExpressions;
using D365.Plugins.Common;
using Microsoft.Xrm.Sdk;

namespace D365.Plugins.Contact
{
    /// <summary>
    /// Cleans and defaults Contact values before they are saved:
    ///  - trims First Name and Last Name and collapses repeated spaces;
    ///  - on Create, sets Preferred Method of Contact to Email when an email is given and no method is chosen.
    /// Runs in PreOperation, so changing Target saves the values in the same write (no extra Update).
    ///
    /// Register:
    ///   Message: Create | Table: contact | Stage: PreOperation (20) | Mode: Synchronous
    ///   Message: Update | Table: contact | Stage: PreOperation (20) | Mode: Synchronous
    ///                     Filtering attributes: firstname, lastname
    /// </summary>
    public class ContactDefaultsPlugin : PluginBase
    {
        // contact.preferredcontactmethodcode: 1 Any, 2 Email, 3 Phone, 4 Fax, 5 Mail
        private const int PreferredContactMethodEmail = 2;
        private static readonly Regex MultipleSpaces = new Regex(@"\s{2,}", RegexOptions.Compiled);

        protected override void ExecutePlugin(LocalPluginContext localContext)
        {
            var context = localContext.PluginExecutionContext;
            if (context.PrimaryEntityName != "contact" || context.Stage != PipelineStage.PreOperation)
            {
                localContext.Trace("Registered on an unexpected step; nothing to do.");
                return;
            }

            var target = localContext.GetTargetEntity();
            if (target == null)
            {
                return;
            }

            CleanName(localContext, target, "firstname");
            CleanName(localContext, target, "lastname");

            if (context.MessageName == "Create"
                && target.GetAttributeValue<OptionSetValue>("preferredcontactmethodcode") == null
                && !string.IsNullOrWhiteSpace(target.GetAttributeValue<string>("emailaddress1")))
            {
                target["preferredcontactmethodcode"] = new OptionSetValue(PreferredContactMethodEmail);
                localContext.Trace("Preferred Method of Contact defaulted to Email.");
            }
        }

        private static void CleanName(LocalPluginContext localContext, Entity target, string attribute)
        {
            if (!target.Contains(attribute))
            {
                return;
            }

            var value = target.GetAttributeValue<string>(attribute);
            if (value == null)
            {
                return;
            }

            var cleaned = MultipleSpaces.Replace(value.Trim(), " ");
            if (cleaned != value)
            {
                target[attribute] = cleaned;
                localContext.Trace("{0} cleaned from '{1}' to '{2}'.", attribute, value, cleaned);
            }
        }
    }
}
