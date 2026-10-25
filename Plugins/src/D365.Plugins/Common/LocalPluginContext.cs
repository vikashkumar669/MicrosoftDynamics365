using System;
using Microsoft.Xrm.Sdk;

namespace D365.Plugins.Common
{
    /// <summary>
    /// Wraps the services the Dataverse pipeline passes to a plugin, so each plugin
    /// gets them in one line and in the same way.
    /// </summary>
    public sealed class LocalPluginContext
    {
        private IOrganizationService _systemService;

        public LocalPluginContext(IServiceProvider serviceProvider)
        {
            if (serviceProvider == null)
            {
                throw new InvalidPluginExecutionException("serviceProvider is null.");
            }

            ServiceProvider = serviceProvider;
            PluginExecutionContext = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));
            TracingService = (ITracingService)serviceProvider.GetService(typeof(ITracingService));
            ServiceFactory = (IOrganizationServiceFactory)serviceProvider.GetService(typeof(IOrganizationServiceFactory));

            // Runs as the user the step is configured to run as (context.UserId).
            OrganizationService = ServiceFactory.CreateOrganizationService(PluginExecutionContext.UserId);
        }

        public IServiceProvider ServiceProvider { get; private set; }

        public IPluginExecutionContext PluginExecutionContext { get; private set; }

        public ITracingService TracingService { get; private set; }

        public IOrganizationServiceFactory ServiceFactory { get; private set; }

        /// <summary>Service running as context.UserId.</summary>
        public IOrganizationService OrganizationService { get; private set; }

        /// <summary>
        /// Service running as the SYSTEM user. Use only for checks that must see every
        /// record (for example duplicate detection), never to bypass business security.
        /// </summary>
        public IOrganizationService SystemOrganizationService
        {
            get
            {
                if (_systemService == null)
                {
                    _systemService = ServiceFactory.CreateOrganizationService(null);
                }

                return _systemService;
            }
        }

        public void Trace(string format, params object[] args)
        {
            if (TracingService == null || string.IsNullOrEmpty(format))
            {
                return;
            }

            var message = args == null || args.Length == 0 ? format : string.Format(format, args);

            // Pass the text as an argument so braces inside data (JSON, GUID formats) are never parsed as placeholders.
            TracingService.Trace("{0}", message);
        }

        /// <summary>Returns the Target as an Entity (Create, Update), or null when it is not one.</summary>
        public Entity GetTargetEntity()
        {
            object target;
            if (PluginExecutionContext.InputParameters.TryGetValue("Target", out target))
            {
                return target as Entity;
            }

            return null;
        }

        /// <summary>Returns the Target as an EntityReference (Delete, Assign...), or null.</summary>
        public EntityReference GetTargetReference()
        {
            object target;
            if (PluginExecutionContext.InputParameters.TryGetValue("Target", out target))
            {
                return target as EntityReference;
            }

            return null;
        }

        /// <summary>Returns a registered pre image by alias, or null when it was not registered.</summary>
        public Entity GetPreImage(string alias)
        {
            Entity image;
            return PluginExecutionContext.PreEntityImages.TryGetValue(alias, out image) ? image : null;
        }

        /// <summary>Returns a registered post image by alias, or null when it was not registered.</summary>
        public Entity GetPostImage(string alias)
        {
            Entity image;
            return PluginExecutionContext.PostEntityImages.TryGetValue(alias, out image) ? image : null;
        }

        /// <summary>True when the step runs for the expected table, message and stage.</summary>
        public bool IsStep(string entityName, string messageName, int stage)
        {
            var context = PluginExecutionContext;
            return string.Equals(context.PrimaryEntityName, entityName, StringComparison.OrdinalIgnoreCase)
                && string.Equals(context.MessageName, messageName, StringComparison.OrdinalIgnoreCase)
                && context.Stage == stage;
        }
    }
}
