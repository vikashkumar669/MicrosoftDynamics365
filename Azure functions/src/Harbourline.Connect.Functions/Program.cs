using Harbourline.Connect.Core;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.Hosting;

var builder = FunctionsApplication.CreateBuilder(args);

// ASP.NET Core integration: HttpRequest and IActionResult in functions.
builder.ConfigureFunctionsWebApplication();

// Options, Dataverse client and services shared by every function.
builder.Services.AddHarbourlineCore(builder.Configuration);

builder.Build().Run();
