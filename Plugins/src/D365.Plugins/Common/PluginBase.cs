using System;
using System.ServiceModel;
using Microsoft.Xrm.Sdk;

namespace D365.Plugins.Common
{
    /// <summary>Pipeline stage numbers used when registering steps.</summary>
    public static class PipelineStage
    {
        public const int PreValidation = 10;
        public const int PreOperation = 20;
        public const int MainOperation = 30;
        public const int PostOperation = 40;
    }

    /// <summary>
    /// Base class for every plugin in this assembly: builds the context, traces entry and
    /// exit, and turns unexpected errors into a clear InvalidPluginExecutionException.
    /// Plugins must stay stateless: Dataverse caches and reuses the instance across threads.
    /// </summary>
    public abstract class PluginBase : IPlugin
    {
        protected PluginBase()
        {
        }

        protected PluginBase(string unsecureConfiguration, string secureConfiguration)
        {
            UnsecureConfiguration = unsecureConfiguration;
            SecureConfiguration = secureConfiguration;
        }

        /// <summary>Unsecure configuration from the step registration (readable by anyone who can read the step).</summary>
        protected string UnsecureConfiguration { get; private set; }

        /// <summary>Secure configuration from the step registration (readable by System Administrators only).</summary>
        protected string SecureConfiguration { get; private set; }

        public void Execute(IServiceProvider serviceProvider)
        {
            var localContext = new LocalPluginContext(serviceProvider);
            var context = localContext.PluginExecutionContext;
            var pluginName = GetType().Name;

            localContext.Trace(
                "Entered {0}. Message: {1}, Table: {2}, Stage: {3}, Mode: {4}, Depth: {5}, CorrelationId: {6}",
                pluginName,
                context.MessageName,
                context.PrimaryEntityName,
                context.Stage,
                context.Mode,
                context.Depth,
                context.CorrelationId);

            try
            {
                ExecutePlugin(localContext);
            }
            catch (InvalidPluginExecutionException)
            {
                // Business errors already carry a message meant for the user.
                throw;
            }
            catch (FaultException<OrganizationServiceFault> ex)
            {
                localContext.Trace("OrganizationServiceFault in {0}: {1}", pluginName, ex.ToString());
                throw new InvalidPluginExecutionException(
                    string.Format("{0} could not complete the operation: {1}", pluginName, ex.Detail != null ? ex.Detail.Message : ex.Message),
                    ex);
            }
            catch (Exception ex)
            {
                localContext.Trace("Unexpected error in {0}: {1}", pluginName, ex.ToString());
                throw new InvalidPluginExecutionException(
                    string.Format("An unexpected error occurred in {0}. Check the Plug-in Trace Log for details.", pluginName),
                    ex);
            }
            finally
            {
                localContext.Trace("Exiting {0}.", pluginName);
            }
        }

        /// <summary>Put the plugin's logic here.</summary>
        protected abstract void ExecutePlugin(LocalPluginContext localContext);
    }
}
