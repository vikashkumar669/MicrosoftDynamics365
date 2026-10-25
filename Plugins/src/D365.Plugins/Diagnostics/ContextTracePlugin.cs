using System.Collections.Generic;
using System.Text;
using D365.Plugins.Common;
using Microsoft.Xrm.Sdk;

namespace D365.Plugins.Diagnostics
{
    /// <summary>
    /// Training aid: writes the whole execution context to the Plug-in Trace Log.
    /// Register it on any step you want to inspect, then open Settings > Plug-in Trace Log.
    /// Turn trace logging off (or unregister this step) when you are done: logs use storage.
    ///
    /// Example registration:
    ///   Message: Update | Table: account | Stage: PostOperation (40) | Mode: Asynchronous
    ///   Pre image alias: PreImage (name, accountnumber) | Post image alias: PostImage (name, accountnumber)
    /// </summary>
    public class ContextTracePlugin : PluginBase
    {
        protected override void ExecutePlugin(LocalPluginContext localContext)
        {
            var context = localContext.PluginExecutionContext;
            var text = new StringBuilder();

            text.AppendLine("=== Execution context ===");
            text.AppendLine("MessageName: " + context.MessageName);
            text.AppendLine("PrimaryEntityName: " + context.PrimaryEntityName);
            text.AppendLine("PrimaryEntityId: " + context.PrimaryEntityId);
            text.AppendLine("Stage: " + context.Stage);
            text.AppendLine("Mode: " + (context.Mode == 0 ? "0 (Synchronous)" : context.Mode + " (Asynchronous)"));
            text.AppendLine("Depth: " + context.Depth);
            text.AppendLine("IsInTransaction: " + context.IsInTransaction);
            text.AppendLine("UserId: " + context.UserId);
            text.AppendLine("InitiatingUserId: " + context.InitiatingUserId);
            text.AppendLine("BusinessUnitId: " + context.BusinessUnitId);
            text.AppendLine("OrganizationName: " + context.OrganizationName);
            text.AppendLine("CorrelationId: " + context.CorrelationId);
            text.AppendLine("HasParentContext: " + (context.ParentContext != null));

            AppendParameters(text, "InputParameters", context.InputParameters);
            AppendParameters(text, "OutputParameters", context.OutputParameters);
            AppendParameters(text, "SharedVariables", context.SharedVariables);
            AppendImages(text, "PreEntityImages", context.PreEntityImages);
            AppendImages(text, "PostEntityImages", context.PostEntityImages);

            localContext.Trace(text.ToString());
        }

        private static void AppendParameters(StringBuilder text, string title, ParameterCollection parameters)
        {
            text.AppendLine("--- " + title + " (" + parameters.Count + ") ---");
            foreach (KeyValuePair<string, object> parameter in parameters)
            {
                var entity = parameter.Value as Entity;
                if (entity != null)
                {
                    AppendEntity(text, parameter.Key, entity);
                }
                else
                {
                    text.AppendLine(parameter.Key + ": " + Describe(parameter.Value));
                }
            }
        }

        private static void AppendImages(StringBuilder text, string title, EntityImageCollection images)
        {
            text.AppendLine("--- " + title + " (" + images.Count + ") ---");
            foreach (KeyValuePair<string, Entity> image in images)
            {
                AppendEntity(text, image.Key, image.Value);
            }
        }

        private static void AppendEntity(StringBuilder text, string label, Entity entity)
        {
            text.AppendLine(label + ": Entity " + entity.LogicalName + " " + entity.Id);
            foreach (KeyValuePair<string, object> attribute in entity.Attributes)
            {
                text.AppendLine("    " + attribute.Key + " = " + Describe(attribute.Value));
            }
        }

        private static string Describe(object value)
        {
            if (value == null)
            {
                return "(null)";
            }

            var reference = value as EntityReference;
            if (reference != null)
            {
                return "EntityReference " + reference.LogicalName + " " + reference.Id + (reference.Name != null ? " (" + reference.Name + ")" : string.Empty);
            }

            var option = value as OptionSetValue;
            if (option != null)
            {
                return "OptionSetValue " + option.Value;
            }

            var money = value as Money;
            if (money != null)
            {
                return "Money " + money.Value;
            }

            return value.GetType().Name + " " + value;
        }
    }
}
