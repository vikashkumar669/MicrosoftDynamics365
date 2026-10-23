using Azure.Core;
using Microsoft.Extensions.Logging;
using Microsoft.PowerPlatform.Dataverse.Client;

namespace Harbourline.Connect.Core.Dataverse;

/// <summary>
/// Creates a <see cref="ServiceClient"/> that gets its access tokens
/// from an Azure <see cref="TokenCredential"/> instead of a secret.
/// With DefaultAzureCredential this is your az login on a laptop and
/// the Function App's managed identity in Azure.
/// </summary>
public static class DataverseClientFactory
{
    public static ServiceClient Create(
        DataverseOptions options,
        TokenCredential credential,
        ILogger logger)
    {
        ArgumentNullException.ThrowIfNull(options);
        ArgumentNullException.ThrowIfNull(credential);

        var instanceUrl = new Uri(options.Url);
        string[] scopes =
        [
            instanceUrl.GetLeftPart(UriPartial.Authority) + "/.default"
        ];

        return new ServiceClient(
            instanceUrl,
            async _ =>
            {
                var token = await credential
                    .GetTokenAsync(
                        new TokenRequestContext(scopes),
                        CancellationToken.None)
                    .ConfigureAwait(false);
                return token.Token;
            },
            useUniqueInstance: true,
            logger: logger);
    }
}
