"""Draws the book's architecture diagrams (chapters 3-25).

    ICON_DIR=/path/to/icons python3 book/figures/make_figures.py [ch07 ...]

Each function draws one figure with book/build/diagram.py, which
measures every label and fails if one does not fit. Icons come from the
author's local copy of Microsoft's Azure, Dynamics 365 and Power Platform
icon sets (not committed to the repository).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "build"))

import diagram as D  # noqa: E402

FIGS = {}


def fig(chapter, name):
    def wrap(fn):
        FIGS[(chapter, name)] = fn
        return fn
    return wrap


def out(chapter, name):
    folder = os.path.join(HERE, chapter)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, name)


# --------------------------------------------------------------- ch03
@fig("ch03", "devloop")
def ch03_devloop():
    d = D.Diagram(640, 330, "On a laptop the Functions host runs your "
                  "code, Azurite stands in for storage, and your own "
                  "sign-in reaches a developer Dataverse environment")
    d.container(10, 10, 400, 270, "Your laptop")
    d.node(30, 50, 170, 56, "VS Code or", ["Visual Studio"], kind="ms")
    d.node(30, 130, 170, 64, "Core Tools", ["func start", "host on :7071"],
           kind="ms", icon="functions")
    d.node(220, 130, 170, 64, "Harbourline", ["Connect (.NET 10)"],
           kind="ours")
    d.node(30, 214, 170, 50, "Azurite", ["local storage"], kind="ms",
           icon="storage")
    d.node(220, 214, 170, 50, "Mock APIs", ["LedgerOne, SignBridge"],
           kind="ext")
    d.arrow([(115, 106), (115, 126)], label=None)
    d.arrow([(200, 162), (216, 162)])
    d.arrow([(115, 194), (115, 210)])
    d.arrow([(305, 194), (305, 210)])
    d.node(450, 50, 180, 56, "Azure CLI", ["az login"], kind="ms")
    d.node(450, 140, 180, 64, "Microsoft Entra ID", ["token for you"],
           kind="ms", icon="appregistration")
    d.node(450, 236, 180, 64, "Dataverse", ["developer environment"],
           kind="ms", icon="dataverse")
    d.arrow([(540, 106), (540, 136)])
    d.arrow([(540, 204), (540, 232)])
    d.arrow([(390, 150), (446, 150)], kind="async", label="token",
            at=(418, 144))
    d.arrow([(390, 180), (430, 180), (430, 262), (446, 262)],
            label="SDK", at=(430, 226))
    d.legend(318, [("ours", "our code"), ("ext", "local stand-in"),
                   ("async", "token request")])
    d.save(out("ch03", "devloop"))
    return d


# --------------------------------------------------------------- ch04
@fig("ch04", "apis")
def ch04_apis():
    d = D.Diagram(640, 300, "The SDK for .NET and the Web API are two "
                  "doors into the same Dataverse services")
    d.node(10, 40, 190, 64, "QueryExpression", ["typed C# objects"],
           kind="ours")
    d.node(10, 124, 190, 64, "FetchXML", ["XML query string"],
           kind="ours")
    d.node(10, 208, 190, 64, "OData query", ["$select, $filter …"],
           kind="ours")
    d.node(240, 70, 170, 90, "ServiceClient",
           ["SDK for .NET", "retries, throttling"], kind="ms")
    d.node(240, 196, 170, 64, "HttpClient", ["your own code"], kind="ms")
    d.container(440, 30, 190, 250, "Dataverse")
    d.node(455, 80, 160, 56, "Organization", ["service"], kind="ms")
    d.node(455, 196, 160, 56, "Web API", ["OData v4, REST"], kind="ms")
    d.arrow([(200, 72), (236, 96)])
    d.arrow([(200, 156), (236, 134)])
    d.arrow([(200, 240), (236, 232)])
    d.arrow([(410, 108), (451, 108)])
    d.arrow([(410, 226), (451, 226)])
    d.text(455, 160, "same tables, security,", 11)
    d.text(455, 175, "plug-ins and limits", 11)
    d.save(out("ch04", "apis"))
    return d


# --------------------------------------------------------------- ch05
@fig("ch05", "identity")
def ch05_identity():
    d = D.Diagram(640, 340, "Locally your developer sign-in, in Azure the "
                  "managed identity: the same code gets a token either "
                  "way, and Dataverse decides what it may do")
    d.node(10, 30, 180, 64, "DefaultAzure", ["Credential"], kind="ours")
    d.node(10, 130, 180, 56, "Laptop", ["Azure CLI sign-in"], kind="ms")
    d.node(10, 220, 180, 64, "Function App", ["managed identity"],
           kind="ms", icon="managedidentity")
    d.arrow([(100, 94), (100, 126)], label="tries in order",
            at=(100, 116))
    d.arrow([(100, 186), (100, 216)])
    d.container(230, 20, 160, 280, "Microsoft Entra ID",
                kind="boundary")
    d.node(245, 80, 130, 64, "Access token", ["for <org>/.default"],
           kind="ms")
    d.node(245, 190, 130, 64, "Key Vault", ["other secrets"],
           kind="ms", icon="keyvault")
    d.arrow([(190, 252), (215, 252), (215, 112), (241, 112)],
            label="ask", at=(215, 180))
    d.container(420, 20, 210, 280, "Dataverse environment")
    d.node(435, 60, 180, 64, "Application user", ["mapped to the",
                                                  "identity"], kind="ms")
    d.node(435, 150, 180, 64, "Security role", ["Harbourline", "Integration"],
           kind="ms")
    d.node(435, 230, 180, 56, "Tables", ["hl_property …"], kind="ms",
           icon="dataverse")
    d.arrow([(375, 112), (431, 92)], label="bearer", at=(400, 94))
    d.arrow([(525, 124), (525, 146)])
    d.arrow([(525, 214), (525, 226)])
    d.legend(326, [("ours", "our code"), ("boundary", "trust boundary")])
    d.save(out("ch05", "identity"))
    return d


# --------------------------------------------------------------- ch07
@fig("ch07", "pipeline")
def ch07_pipeline():
    d = D.Diagram(640, 250, "Each layer has one job: HTTP details stay in "
                  "the function, rules in the validator, Dataverse in "
                  "the service")
    d.node(10, 70, 110, 64, "Portal", ["caller"], kind="ext")
    d.node(150, 50, 140, 104, "PropertyFunctions",
           ["parse request", "map Outcome", "to HTTP"], kind="ours",
           title_size=12)
    d.node(320, 30, 140, 56, "Validator", ["all errors"], kind="ours")
    d.node(320, 118, 140, 56, "PropertyService", ["query, update"],
           kind="ours", title_size=12)
    d.node(500, 118, 130, 56, "Dataverse", ["hl_property"], kind="ms",
           icon="dataverse")
    d.arrow([(120, 102), (146, 102)])
    d.arrow([(290, 80), (316, 62)])
    d.arrow([(290, 128), (316, 140)])
    d.arrow([(460, 146), (496, 146)])
    d.arrow([(570, 174), (570, 214), (220, 214), (220, 158)],
            kind="fail", label="404 · 409 · 412 as Outcome", at=(395, 218))
    d.legend(246, [("ours", "our code"), ("ext", "caller"),
                   ("fail", "failure path")])
    d.save(out("ch07", "pipeline"))
    return d


@fig("ch07", "etag")
def ch07_etag():
    d = D.Diagram(640, 300, "Optimistic concurrency: the second writer's "
                  "If-Match no longer matches, so Dataverse refuses the "
                  "update and the API returns 412")
    cols = [(80, "Agent A"), (250, "Agent B"), (420, "Property API"),
            (570, "Dataverse")]
    for x, label in cols:
        d.text(x, 22, label, 12.5, 600, D.NAVY, "middle")
        d.parts.append(f'<path d="M{x} 32V290" stroke="{D.SOFT}" '
                       f'stroke-width="1.2"/>')
    d.arrow([(80, 60), (416, 60)], label="GET HBR-0042", at=(250, 54))
    d.arrow([(420, 84), (84, 84)], label="200, ETag \"1001\"",
            at=(250, 78))
    d.arrow([(250, 112), (416, 112)], label="GET → ETag \"1001\"",
            at=(330, 106))
    d.arrow([(250, 146), (416, 146)], label="PATCH, If-Match \"1001\"",
            at=(330, 140))
    d.arrow([(420, 170), (566, 170)], label="update, version 1001",
            at=(495, 164))
    d.arrow([(570, 194), (424, 194)], label="ok → 1002", at=(495, 188))
    d.arrow([(80, 230), (416, 230)], label="PATCH, If-Match \"1001\"",
            at=(250, 224))
    d.arrow([(420, 252), (566, 252)], label="version mismatch",
            kind="fail", at=(495, 246))
    d.arrow([(416, 276), (84, 276)], kind="fail",
            label="412 Precondition Failed", at=(250, 270))
    d.save(out("ch07", "etag"))
    return d


# --------------------------------------------------------------- ch08
@fig("ch08", "resilience")
def ch08_resilience():
    d = D.Diagram(640, 300, "A request passes through nested resilience "
                  "strategies before it reaches LedgerOne; each one "
                  "handles a different kind of failure")
    d.node(10, 120, 100, 60, "LedgerOne", ["Client"], kind="ours")
    layers = [
        (130, 20, 380, 260, "Total timeout · 45 s"),
        (150, 50, 340, 210, "Retry · 3 times, backoff + jitter"),
        (170, 80, 300, 160, "Circuit breaker · opens on failures"),
        (190, 110, 260, 110, "Attempt timeout · 10 s"),
    ]
    for x, y, w, h, label in layers:
        d.container(x, y, w, h, label)
    d.node(215, 150, 210, 50, "HttpClientHandler", ["one HTTP attempt"],
           kind="ms")
    d.node(530, 120, 100, 60, "LedgerOne", ["API"], kind="ext")
    d.arrow([(110, 150), (211, 175)])
    d.arrow([(425, 175), (526, 150)])
    d.arrow([(580, 180), (580, 290), (320, 290), (320, 204)],
            kind="fail", label="429 · 5xx · timeout → retry",
            at=(450, 286))
    d.save(out("ch08", "resilience"))
    return d


# --------------------------------------------------------------- ch09
@fig("ch09", "paths")
def ch09_paths():
    d = D.Diagram(640, 330, "Four ways a Dataverse event can reach a "
                  "function; Harbourline uses the asynchronous webhook "
                  "and hands slow work to a queue")
    d.node(10, 130, 120, 70, "Dataverse", ["lease", "updated"],
           kind="ms", icon="dataverse")
    rows = [
        (20, "Webhook step", "sync or async · 60 s", "ours-path"),
        (100, "Service Bus endpoint", "async only", None),
        (180, "Plug-in calling out", "your C# · 2 min", None),
        (260, "Power Automate flow", "custom connector", None),
    ]
    for y, title, sub, _ in rows:
        d.node(180, y, 190, 56, title, [sub],
               kind="accent" if y == 20 else "ms", title_size=12)
        d.arrow([(130, 165), (155, 165), (155, y + 28), (176, y + 28)])
    d.node(420, 20, 210, 56, "LeaseStatusWebhook", ["HTTP function"],
           kind="ours")
    d.node(420, 100, 210, 56, "Service Bus queue", ["lease-signing"],
           kind="ms", icon="servicebus")
    d.node(420, 180, 210, 56, "Any HTTPS endpoint", ["e.g. a function"],
           kind="ms")
    d.node(420, 260, 210, 56, "API Management", ["→ functions"],
           kind="ms", icon="apim")
    d.arrow([(370, 48), (416, 48)])
    d.arrow([(525, 76), (525, 96)], label="queues work", at=(575, 90))
    d.arrow([(370, 128), (416, 128)])
    d.arrow([(370, 208), (416, 208)])
    d.arrow([(370, 288), (416, 288)])
    d.save(out("ch09", "paths"))
    return d


# --------------------------------------------------------------- ch10
@fig("ch10", "watermark")
def ch10_watermark():
    d = D.Diagram(640, 260, "Each run reads from the last saved watermark "
                  "minus a five-minute overlap, and saves a new watermark "
                  "only when every row succeeded")
    d.parts.append(f'<path d="M20 120H620" stroke="{D.SLATE}" '
                   f'stroke-width="1.5" marker-end="url(#a)"/>')
    d.text(620, 106, "time (UTC)", 11, anchor="end")
    for x, label in [(120, "Mon 02:00"), (330, "Tue 02:00"),
                     (540, "Wed 02:00")]:
        d.parts.append(f'<path d="M{x} 112V128" stroke="{D.NAVY}" '
                       f'stroke-width="2"/>')
        d.text(x, 146, label, 11, 600, D.NAVY, "middle")
    d.parts.append(f'<rect x="96" y="70" width="234" height="30" rx="4" '
                   f'fill="{D.SKY}" stroke="{D.AZURE}"/>')
    d.text(213, 90, "Tue run reads this window", 11, 600, D.NAVY, "middle")
    d.parts.append(f'<rect x="96" y="104" width="24" height="12" '
                   f'fill="#FFE2B8"/>')
    d.text(60, 60, "5 min overlap", 11, 600, D.AMBER, "start")
    d.arrow([(100, 64), (106, 102)], kind="fail")
    d.node(150, 190, 170, 56, "Every row ok", ["save new watermark"],
           kind="ours")
    d.node(350, 190, 190, 56, "Any row failed", ["keep old watermark;",
                                                  "next run retries"],
           kind="warn")
    d.arrow([(330, 154), (330, 170), (235, 170), (235, 186)])
    d.arrow([(330, 170), (445, 170), (445, 186)], kind="fail")
    d.save(out("ch10", "watermark"))
    return d


# --------------------------------------------------------------- ch11
@fig("ch11", "topic")
def ch11_topic():
    d = D.Diagram(640, 300, "Dataverse publishes each account change once; "
                  "every subscription gets its own copy, and messages "
                  "that keep failing move to that subscription's "
                  "dead-letter queue")
    d.node(10, 110, 120, 70, "Dataverse", ["account", "changes"],
           kind="ms", icon="dataverse")
    d.container(160, 20, 250, 250, "Service Bus topic: account-events")
    d.node(180, 70, 210, 56, "Subscription", ["ledgerone"], kind="ms",
           icon="servicebus")
    d.node(180, 180, 210, 56, "Subscription", ["audit (future)"],
           kind="note")
    d.arrow([(130, 145), (155, 145), (155, 98), (176, 98)],
            label="SAS: Send only", at=(150, 60), anchor="middle")
    d.arrow([(155, 145), (155, 208), (176, 208)])
    d.node(440, 40, 190, 64, "AccountEvents", ["ToLedgerOne"],
           kind="ours")
    d.node(440, 140, 190, 56, "LedgerOne", ["customers"], kind="ext")
    d.node(440, 224, 190, 56, "Dead-letter queue", ["ledgerone/$DLQ"],
           kind="warn")
    d.arrow([(390, 90), (436, 72)], label="identity", at=(413, 70))
    d.arrow([(535, 104), (535, 136)])
    d.arrow([(390, 110), (420, 110), (420, 252), (436, 252)],
            kind="fail", label="permanent or 10th failure", at=(420, 210))
    d.save(out("ch11", "topic"))
    return d


# --------------------------------------------------------------- ch12
@fig("ch12", "signing")
def ch12_signing():
    d = D.Diagram(640, 330, "The orchestration sends the envelope, then "
                  "waits for SignBridge's callback or a reminder timer, "
                  "for up to nine days, without running any code while "
                  "it waits")
    d.node(10, 20, 150, 56, "lease-signing", ["queue (Ch. 9)"],
           kind="ms", icon="servicebus")
    d.node(10, 110, 150, 56, "Client function", ["StartLeaseSigning"],
           kind="ours")
    d.arrow([(85, 76), (85, 106)])
    d.container(190, 10, 280, 310, "LeaseSigningOrchestration")
    d.node(210, 50, 240, 50, "SendEnvelope", ["activity, retried"],
           kind="ours")
    d.node(210, 130, 240, 64, "Wait for first of:",
           ["SignatureCompleted event", "timer (3 days)"], kind="accent")
    d.node(210, 230, 110, 60, "Signed?", ["Active /", "Declined"],
           kind="ours")
    d.node(340, 230, 110, 60, "Timer", ["remind, or", "expire"],
           kind="ours")
    d.arrow([(160, 138), (185, 138), (185, 75), (206, 75)],
            label="schedule", at=(185, 150))
    d.arrow([(330, 100), (330, 126)])
    d.arrow([(290, 194), (265, 226)])
    d.arrow([(370, 194), (395, 226)])
    d.arrow([(395, 230), (460, 162), (452, 162)], kind="async",
            label="loop", at=(462, 214))
    d.node(500, 50, 130, 56, "SignBridge", ["envelopes"], kind="ext")
    d.node(500, 140, 130, 64, "SignBridge", ["Callback", "(HMAC)"],
           kind="ours")
    d.arrow([(450, 75), (496, 75)])
    d.arrow([(565, 106), (565, 136)], label="tenant signs",
            at=(565, 124))
    d.arrow([(500, 172), (454, 162)], label="raise event", at=(478, 150))
    d.save(out("ch12", "signing"))
    return d


# --------------------------------------------------------------- ch13
@fig("ch13", "feeds")
def ch13_feeds():
    d = D.Diagram(640, 300, "A dropped file raises a blob event; the "
                  "function streams it, upserts the valid rows and "
                  "always writes a report, while unreadable files go to "
                  "quarantine")
    d.node(10, 30, 130, 56, "Partner", ["SFTP / upload"], kind="ext")
    d.node(10, 120, 130, 64, "Blob storage", ["property-feeds"],
           kind="ms")
    d.node(10, 220, 130, 56, "Event Grid", ["BlobCreated"], kind="ms",
           icon="eventgrid")
    d.arrow([(75, 86), (75, 116)])
    d.arrow([(75, 184), (75, 216)])
    d.node(180, 120, 200, 64, "ImportPropertyFeed",
           ["blob trigger (Event Grid)"], kind="ours", title_size=12)
    d.arrow([(140, 248), (160, 248), (160, 152), (176, 152)],
            label="webhook", at=(160, 210))
    d.node(180, 30, 200, 56, "Reader + validator",
           ["CSV · JSON · XML, streamed"], kind="ours")
    d.arrow([(280, 120), (280, 90)], both=True)
    d.node(420, 30, 210, 56, "Dataverse", ["UpsertMultiple by code"],
           kind="ms", icon="dataverse")
    d.node(420, 120, 210, 56, "feed-reports", ["<name>.report.csv"],
           kind="ms", icon="blob")
    d.node(420, 210, 210, 56, "feed-quarantine", ["unreadable files"],
           kind="warn")
    d.arrow([(380, 140), (416, 70)], label="valid rows", at=(398, 98))
    d.arrow([(380, 152), (416, 148)])
    d.arrow([(380, 170), (400, 170), (400, 238), (416, 238)],
            kind="fail", label="bad file", at=(400, 210))
    d.save(out("ch13", "feeds"))
    return d


def main(argv):
    wanted = set(argv)
    used = set()
    for (chapter, name), fn in FIGS.items():
        if wanted and chapter not in wanted:
            continue
        d = fn()
        used |= d.icons_used
        print(f"{chapter}/{name}: ok")
    print("icons used:", ", ".join(sorted(used)) or "none")


if __name__ == "__main__":
    main(sys.argv[1:])
