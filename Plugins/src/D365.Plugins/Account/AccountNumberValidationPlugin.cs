using System.Text.RegularExpressions;
using D365.Plugins.Common;
using Microsoft.Xrm.Sdk;

namespace D365.Plugins.Account
{
    /// <summary>
    /// Rejects an Account whose Account Number is missing or not in the format ACC-12345.
    ///
    /// Register:
    ///   Message: Create   | Table: account | Stage: PreValidation (10) | Mode: Synchronous
    ///   Message: Update   | Table: account | Stage: PreValidation (10) | Mode: Synchronous
    ///                       Filtering attributes: accountnumber
    /// </summary>
    public class AccountNumberValidationPlugin : PluginBase
    {
        private const string AccountNumberAttribute = "accountnumber";
        private static readonly Regex AccountNumberPattern = new Regex(@"^ACC-\d{5}$", RegexOptions.Compiled);

        protected override void ExecutePlugin(LocalPluginContext localContext)
        {
            var context = localContext.PluginExecutionContext;
            if (context.PrimaryEntityName != "account" || context.Stage != PipelineStage.PreValidation)
            {
                localContext.Trace("Registered on an unexpected step; nothing to do.");
                return;
            }

            var target = localContext.GetTargetEntity();
            if (target == null)
            {
                return;
            }

            var isCreate = context.MessageName == "Create";

            // On Update, Target only holds changed columns: skip when Account Number didn't change.
            if (!isCreate && !target.Contains(AccountNumberAttribute))
            {
                return;
            }

            var accountNumber = target.GetAttributeValue<string>(AccountNumberAttribute);
            if (string.IsNullOrWhiteSpace(accountNumber))
            {
                throw new InvalidPluginExecutionException("Account Number is required. Use the format ACC-12345.");
            }

            accountNumber = accountNumber.Trim();
            if (!AccountNumberPattern.IsMatch(accountNumber))
            {
                throw new InvalidPluginExecutionException(
                    string.Format("Account Number '{0}' is not valid. Use the format ACC-12345 (ACC- followed by 5 digits).", accountNumber));
            }

            localContext.Trace("Account Number {0} is valid.", accountNumber);
        }
    }
}
