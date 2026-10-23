using Azure.Core;
using Azure.Identity;
using Harbourline.Connect.Core.Dataverse;
using Harbourline.Connect.Core.Health;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Microsoft.PowerPlatform.Dataverse.Client;

namespace Harbourline.Connect.Core;

public static class ServiceCollectionExtensions
{
    /// <summary>
    /// Registers Harbourline Connect services. The Dataverse client is a
    /// singleton: creating one is expensive, and it is thread-safe.
    /// </summary>
    public static IServiceCollection AddHarbourlineCore(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        ArgumentNullException.ThrowIfNull(configuration);

        services.TryAddSingleton(TimeProvider.System);
        services.TryAddSingleton<HealthService>();

        // <listing:dataverse-registration>
        services.AddOptions<DataverseOptions>()
            .Bind(configuration.GetSection(
                DataverseOptions.SectionName))
            .ValidateDataAnnotations()                 // <1>
            .ValidateOnStart();

        services.TryAddSingleton<TokenCredential>(
            _ => new DefaultAzureCredential());        // <2>

        services.TryAddSingleton(sp =>                 // <3>
            DataverseClientFactory.Create(
                sp.GetRequiredService<
                    IOptions<DataverseOptions>>().Value,
                sp.GetRequiredService<TokenCredential>(),
                sp.GetRequiredService<
                    ILogger<ServiceClient>>()));

        services.TryAddSingleton<IOrganizationServiceAsync2>(
            sp => sp.GetRequiredService<ServiceClient>()); // <4>
        // </listing:dataverse-registration>

        return services;
    }
}
