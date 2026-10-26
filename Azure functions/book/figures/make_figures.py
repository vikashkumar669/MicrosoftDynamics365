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
    d.node(245, 80, 130, 64, "Token", ["scope: org/.default"], kind="ms",
           icon="appregistration")
    d.node(245, 190, 130, 64, "Key Vault", ["secrets for", "others"],
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
