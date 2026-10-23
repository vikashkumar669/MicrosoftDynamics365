using Harbourline.Connect.Core.Health;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;

namespace Harbourline.Connect.Functions.Functions;

/// <summary>
/// GET /api/health – a liveness check that does not touch Dataverse,
/// so it stays green even when a downstream system is unavailable.
/// </summary>
public sealed class HealthFunction(HealthService health)
{
    [Function("Health")]
    public IActionResult Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get",
            Route = "health")] HttpRequest request)
    {
        ArgumentNullException.ThrowIfNull(request);
        return new OkObjectResult(health.GetStatus());
    }
}
