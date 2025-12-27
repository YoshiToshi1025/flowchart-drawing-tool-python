import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass(frozen=True)
class Node:
    node_id: str
    kind: str           # terminator / process / decision / io / unknown
    title: str
    raw: str            # e.g. "A(開始)"

@dataclass(frozen=True)
class Link:
    src: str
    dst: str
    label: Optional[str]  # None if no label

NODE_RE = re.compile(
    r"""
    ^\s*
    (?P<id>[A-Za-z][A-Za-z0-9_]*)      # node id (A, B, AA, ...)
    \s*
    (?:
        \((?P<title_paren>[^)]*)\)     # (title)
      | \[(?P<title_bracket>[^\]]*)\]  # [title]
      | \{(?P<title_brace>[^}]*)\}     # {title}
      | /(?P<title_slash>[^/]*)/      # /title/
    )
    \s*$
    """,
    re.VERBOSE,
)

# tokenizes chain links like:
# A --> B --> C --Yes--> D
# Returns sequence of (node_id, edge_label_or_none_to_next)
CHAIN_TOKEN_RE = re.compile(r"""
    (?P<node>[A-Za-z][A-Za-z0-9_]*)
  | --\s*(?P<label>.*?)\s*-->          # labeled edge -- label -->
  | -->
""", re.VERBOSE)

def _node_kind_and_title(m: re.Match) -> Tuple[str, str]:
    if m.group("title_paren") is not None:
        return "terminator", m.group("title_paren").strip()
    if m.group("title_bracket") is not None:
        return "process", m.group("title_bracket").strip()
    if m.group("title_brace") is not None:
        return "decision", m.group("title_brace").strip()
    if m.group("title_slash") is not None:
        return "io", m.group("title_slash").strip()
    return "unknown", ""

def parse_mermaid_flowdata(text: str) -> Tuple[Dict[str, Node], List[Link]]:
    """
    Parse Mermaid flowchart text that contains:
      - node definitions like: A(開始), B[初期化], C{条件?}, D/保存/
      - link chains like: A --> B --> C --Yes--> D
    Returns:
      nodes: dict[node_id] = Node(...)
      links: list of Link(src, link_id, dst)
    """
    nodes: Dict[str, Node] = {}
    links: List[Link] = []

    lines = text.splitlines()

    in_flowchart = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("%%"):
            continue

        # Detect block start (flexible)
        if re.match(r"^flowchart\s+", line):
            in_flowchart = True
            continue
        if not in_flowchart:
            continue

        # Skip Mermaid directives that are not node/link lines
        if line.startswith(("classDef ", "class ", "style ", "linkStyle ", "subgraph ", "end")):
            continue

        # 1) Node line?
        nm = NODE_RE.match(line)
        if nm:
            node_id = nm.group("id")
            kind, title = _node_kind_and_title(nm)
            nodes[node_id] = Node(node_id=node_id, kind=kind, title=title, raw=line)
            continue

        # 2) Link line? (contains -->)
        if "-->" in line:
            links.extend(parse_link_chain_line(line))
            continue

        # otherwise ignore (can extend later)

    return nodes, links

def parse_link_chain_line(line: str) -> List[Link]:
    """
    Parse Mermaid link chains and extract label values.

    Examples:
      A --> B --> C
      A --Yes--> B --> C
      C -- 編集 --> E
    """
    s = line.strip()
    links: List[Link] = []

    node_pat = re.compile(r"\s*([A-Za-z][A-Za-z0-9_]*)\s*")
    edge_pat = re.compile(
        r"""
        \s*
        (
            -->                         # plain
          | --\s*(?P<label>.*?)\s*-->   # labeled
        )
        \s*
        """,
        re.VERBOSE,
    )

    # 最初のノード
    m = node_pat.match(s)
    if not m:
        return links
    cur = m.group(1)
    i = m.end()

    while i < len(s):
        em = edge_pat.match(s, i)
        if not em:
            break

        label = em.group("label")
        label = label.strip() if label is not None else None
        i = em.end()

        nm = node_pat.match(s, i)
        if not nm:
            break
        nxt = nm.group(1)
        i = nm.end()

        links.append(Link(src=cur, dst=nxt, label=label))
        cur = nxt

    return links

def nodes_to_csv_lines(nodes: Dict[str, Node]) -> List[str]:
    """
    Output: node_id,kind,title,kind
    (Your spec repeats node kind twice, so we do that.)
    """
    out = []
    for node_id in sorted(nodes.keys(), key=_mermaid_id_sort_key):
        n = nodes[node_id]
        out.append(f"node_id:{n.node_id}, kind:{n.kind}, title:{n.title}")
    return out

def links_to_csv_lines(links: List[Link]) -> List[str]:
    """
    src,link_id,dst
    """
    lines = []
    for l in links:
        if l.label:
            link_str = f"--label:{l.label}-->"
        else:
            link_str = "-->"
        lines.append(f"src:{l.src} {link_str} dst:{l.dst}")
    return lines

def _mermaid_id_sort_key(node_id: str) -> Tuple[int, str]:
    """
    Sort A..Z, AA..ZZ reasonably.
    If your IDs are always letters (A, B, AA...), this works well enough.
    """
    return (len(node_id), node_id)

if __name__ == "__main__":
    sample = """mermaid
    
    flowchart TD
      A(開始)
      B[ツールの起動]
      C{新規作成or編集?}
      D[作図]
      E/データ読込/
      F[編集]
      G/画像出力/
      H[資料に画像を添付]
      I(終了)

      A --> B --> C --新規作成--> D --> G --> H --> I
      C --編集--> E --> F --> G
    """

    nodes, links = parse_mermaid_flowdata(sample)

    print("### Nodes (CSV lines)")
    for line in nodes_to_csv_lines(nodes):
        print(line)

    print("\n### Links (CSV lines)")
    for line in links_to_csv_lines(links):
        print(line)
