namespace Harbourline.Connect.Contracts.Orders;

// <listing:order-contract>
/// <summary>A service order sent by a maintenance partner (Chapter 24).</summary>
public sealed record OrderSubmission(
    string? OrderNumber,
    string? PropertyCode,
    string? Category,
    decimal? Amount,
    string? PartnerId);

/// <summary>What the intake API returns: accepted, not yet processed.</summary>
public sealed record OrderAccepted(string OrderNumber, string StatusUrl);
// </listing:order-contract>
