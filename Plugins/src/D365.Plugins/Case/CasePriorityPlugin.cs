using System;
using D365.Plugins.Common;
using Microsoft.Xrm.Sdk;

namespace D365.Plugins.Case
{
    /// <summary>
    /// Customer Service: when a Case (incident) is created without a priority and its title
    /// contains a keyword such as "urgent" or "outage", sets Priority to High.
    /// Keywords can be changed in the step's Unsecure Configuration as a comma-separated list.
    ///
    /// Register:
    ///   Message: Create | Table: incident | Stage: PreOperation (20) | Mode: Synchronous
    ///   Unsecure configuration (optional): urgent,outage,down,critical
    /// </summary>
    public class CasePriorityPlugin : PluginBase
    {
        // incident.prioritycode: 1 High, 2 Normal, 3 Low
        private const int PriorityHigh = 1;
        private static readonly string[] DefaultKeywords = { "urgent", "outage", "down", "critical" };

        private readonly string[] _keywords;

        public CasePriorityPlugin()
            : this(null, null)
        {
        }

        public CasePriorityPlugin(string unsecureConfiguration, string secureConfiguration)
            : base(unsecureConfiguration, secureConfiguration)
        {
            // Parsed once per instance; read-only afterwards, so the plugin stays thread-safe.
            _keywords = ParseKeywords(unsecureConfiguration);
        }

        protected override void ExecutePlugin(LocalPluginContext localContext)
        {
            if (!localContext.IsStep("incident", "Create", PipelineStage.PreOperation))
            {
                localContext.Trace("Registered on an unexpected step; nothing to do.");
                return;
            }

            var target = localContext.GetTargetEntity();
            if (target == null)
            {
                return;
            }

            var priority = target.GetAttributeValue<OptionSetValue>("prioritycode");
            if (priority != null && priority.Value == PriorityHigh)
            {
                return;
            }

            var title = target.GetAttributeValue<string>("title");
            if (string.IsNullOrWhiteSpace(title))
            {
                return;
            }

            foreach (var keyword in _keywords)
            {
                if (title.IndexOf(keyword, StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    target["prioritycode"] = new OptionSetValue(PriorityHigh);
                    localContext.Trace("Title contains '{0}'; priority set to High.", keyword);
                    return;
                }
            }
        }

        private static string[] ParseKeywords(string configuration)
        {
            if (string.IsNullOrWhiteSpace(configuration))
            {
                return DefaultKeywords;
            }

            var parts = configuration.Split(new[] { ',', ';' }, StringSplitOptions.RemoveEmptyEntries);
            var keywords = new System.Collections.Generic.List<string>();
            foreach (var part in parts)
            {
                var keyword = part.Trim();
                if (keyword.Length > 0)
                {
                    keywords.Add(keyword);
                }
            }

            return keywords.Count > 0 ? keywords.ToArray() : DefaultKeywords;
        }
    }
}
