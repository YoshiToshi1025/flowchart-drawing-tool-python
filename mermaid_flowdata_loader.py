import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import constants as ct

@dataclass(frozen=True)
class Node:
    node_id: str
    kind: str           # terminator / process / decision / io / unknown
    title: str
    raw: str            # e.g. "A(開始)"
    pos_lr: int|None = None
    pos_tb: int|None = None
    pos_x: int|None = None
    pos_y: int|None = None

@dataclass(frozen=True)
class Link:
    src: str
    dst: str
    label: Optional[str]  # None if no label
    edge_type: str  = ct.EDGE_TYPE_ELBOW # "elbow" or "line"

NODE_RE = re.compile(
    r"""
    ^\s*
    (?P<id>[A-Za-z][A-Za-z0-9_]*)      # node id (A, B, AA, ...)
    \s*
    (?:
        \((?P<title_paren>[^)]*?)\)     # (title)
      | \[(?P<title_bracket>[^\]]*?)\]  # [title]
      | \{(?P<title_brace>[^}]*?)\}     # {title}
      | /(?P<title_slash>[^/]*?)\//       # /title/
      | \((?P<title_paren2>[^)]*?)\),\s*(?P<paren_pos_tb>[-+]?[0-9]+?),\s*(?P<paren_pos_lr>[-+]?[0-9]+?)         # (title), y, x
      | \[(?P<title_bracket2>[^\]]*?)\],\s*(?P<bracket_pos_tb>[-+]?[0-9]+?),\s*(?P<bracket_pos_lr>[-+]?[0-9]+?)  # [title], y, x
      | \{(?P<title_brace2>[^}]*?)\},\s*(?P<brace_pos_tb>[-+]?[0-9]+?),\s*(?P<brace_pos_lr>[-+]?[0-9]+?)         # {title}, y, x
      | /(?P<title_slash2>[^/]*?)\/,\s*(?P<slash_pos_tb>[-+]?[0-9]+?),\s*(?P<slash_pos_lr>[-+]?[0-9]+?)           # /title/, y, x
      | @\{\s*shape:\s*stadium\s*,\s*label:\s*"(?P<title_paren3>[^"]+?)"\s*\}    # @{ shape: statium, label: "title" }
      | @\{\s*shape:\s*rounded\s*,\s*label:\s*"(?P<title_bracket3>[^"]+?)"\s*\}  # @{ shape: rounded, label: "title" }
      | @\{\s*shape:\s*diamond\s*,\s*label:\s*"(?P<title_brace3>[^"]+?)"\s*\}    # @{ shape: diamond, label: "title" }
      | @\{\s*shape:\s*lean-r\s*,\s*label:\s*"(?P<title_slash3>[^"]+?)"\s*\}     # @{ shape: lean-r, label: "title" }
      | @\{\s*shape:\s*cyl\s*,\s*label:\s*"(?P<title_cyl3>[^"]+?)"\s*\}     # @{ shape: cyl, label: "title" }
      | @\{\s*shape:\s*doc\s*,\s*label:\s*"(?P<title_doc3>[^"]+?)"\s*\}     # @{ shape: doc, label: "title" }
      | @\{\s*shape:\s*stadium\s*,\s*label:\s*"(?P<title_paren4>[^"]+?)"\s*,\s*bx:\s*(?P<paren_pos_lr2>[-+]?[0-9]+?)\s*,\s*by:\s*(?P<paren_pos_tb2>[-+]?[0-9]+?)\s*\}        # @{ shape: statium, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*rounded\s*,\s*label:\s*"(?P<title_bracket4>[^"]+?)"\s*,\s*bx:\s*(?P<bracket_pos_lr2>[-+]?[0-9]+?)\s*,\s*by:\s*(?P<bracket_pos_tb2>[-+]?[0-9]+?)\s*\}  # @{ shape: rounded, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*diamond\s*,\s*label:\s*"(?P<title_brace4>[^"]+?)"\s*,\s*bx:\s*(?P<brace_pos_lr2>[-+]?[0-9]+?)\s*,\s*by:\s*(?P<brace_pos_tb2>[-+]?[0-9]+?)\s*\}        # @{ shape: diamond, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*lean-r\s*,\s*label:\s*"(?P<title_slash4>[^"]+?)"\s*,\s*bx:\s*(?P<slash_pos_lr2>[-+]?[0-9]+?)\s*,\s*by:\s*(?P<slash_pos_tb2>[-+]?[0-9]+?)\s*\}         # @{ shape: lean-r, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*cyl\s*,\s*label:\s*"(?P<title_cyl4>[^"]+?)"\s*,\s*bx:\s*(?P<cyl_pos_lr2>[-+]?[0-9]+?)\s*,\s*by:\s*(?P<cyl_pos_tb2>[-+]?[0-9]+?)\s*\}                  # @{ shape: cyl, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*doc\s*,\s*label:\s*"(?P<title_doc4>[^"]+?)"\s*,\s*bx:\s*(?P<doc_pos_lr2>[-+]?[0-9]+?)\s*,\s*by:\s*(?P<doc_pos_tb2>[-+]?[0-9]+?)\s*\}                  # @{ shape: doc, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*stadium\s*,\s*label:\s*"(?P<title_paren5>[^"]+?)"\s*,\s*x:\s*(?P<paren_pos_x>[-+]?[0-9]+?)\s*,\s*y:\s*(?P<paren_pos_y>[-+]?[0-9]+?)\s*\}        # @{ shape: statium, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*rounded\s*,\s*label:\s*"(?P<title_bracket5>[^"]+?)"\s*,\s*x:\s*(?P<bracket_pos_x>[-+]?[0-9]+?)\s*,\s*y:\s*(?P<bracket_pos_y>[-+]?[0-9]+?)\s*\}  # @{ shape: rounded, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*diamond\s*,\s*label:\s*"(?P<title_brace5>[^"]+?)"\s*,\s*x:\s*(?P<brace_pos_x>[-+]?[0-9]+?)\s*,\s*y:\s*(?P<brace_pos_y>[-+]?[0-9]+?)\s*\}        # @{ shape: diamond, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*lean-r\s*,\s*label:\s*"(?P<title_slash5>[^"]+?)"\s*,\s*x:\s*(?P<slash_pos_x>[-+]?[0-9]+?)\s*,\s*y:\s*(?P<slash_pos_y>[-+]?[0-9]+?)\s*\}         # @{ shape: lean-r, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*cyl\s*,\s*label:\s*"(?P<title_cyl5>[^"]+?)"\s*,\s*x:\s*(?P<cyl_pos_x>[-+]?[0-9]+?)\s*,\s*y:\s*(?P<cyl_pos_y>[-+]?[0-9]+?)\s*\}                  # @{ shape: cyl, label: "title", bx: 999, by: 999 }
      | @\{\s*shape:\s*doc\s*,\s*label:\s*"(?P<title_doc5>[^"]+?)"\s*,\s*x:\s*(?P<doc_pos_x>[-+]?[0-9]+?)\s*,\s*y:\s*(?P<doc_pos_y>[-+]?[0-9]+?)\s*\}                  # @{ shape: doc, label: "title", bx: 999, by: 999 }
    )
    \s*$
    """,
    re.VERBOSE,
)

def _node_kind_and_title(m: re.Match) -> Tuple[str, str]:
    if m.group("title_paren") is not None:
        return "terminator", m.group("title_paren").strip()
    if m.group("title_bracket") is not None:
        return "process", m.group("title_bracket").strip()
    if m.group("title_brace") is not None:
        return "decision", m.group("title_brace").strip()
    if m.group("title_slash") is not None:
        return "io", m.group("title_slash").strip()

    if m.group("title_paren2") is not None:
        return "terminator", m.group("title_paren2").strip()
    if m.group("title_bracket2") is not None:
        return "process", m.group("title_bracket2").strip()
    if m.group("title_brace2") is not None:
        return "decision", m.group("title_brace2").strip()
    if m.group("title_slash2") is not None:
        return "io", m.group("title_slash2").strip()

    if m.group("title_paren3") is not None:
        return "terminator", m.group("title_paren3").strip()
    if m.group("title_bracket3") is not None:
        return "process", m.group("title_bracket3").strip()
    if m.group("title_brace3") is not None:
        return "decision", m.group("title_brace3").strip()
    if m.group("title_slash3") is not None:
        return "io", m.group("title_slash3").strip()
    if m.group("title_cyl3") is not None:
        return "storage", m.group("title_cyl3").strip()
    if m.group("title_doc3") is not None:
        return "document", m.group("title_doc3").strip()

    if m.group("title_paren4") is not None:
        return "terminator", m.group("title_paren4").strip()
    if m.group("title_bracket4") is not None:
        return "process", m.group("title_bracket4").strip()
    if m.group("title_brace4") is not None:
        return "decision", m.group("title_brace4").strip()
    if m.group("title_slash4") is not None:
        return "io", m.group("title_slash4").strip()
    if m.group("title_cyl4") is not None:
        return "storage", m.group("title_cyl4").strip()
    if m.group("title_doc4") is not None:
        return "document", m.group("title_doc4").strip()

    if m.group("title_paren5") is not None:
        return "terminator", m.group("title_paren5").strip()
    if m.group("title_bracket5") is not None:
        return "process", m.group("title_bracket5").strip()
    if m.group("title_brace5") is not None:
        return "decision", m.group("title_brace5").strip()
    if m.group("title_slash5") is not None:
        return "io", m.group("title_slash5").strip()
    if m.group("title_cyl5") is not None:
        return "storage", m.group("title_cyl5").strip()
    if m.group("title_doc5") is not None:
        return "document", m.group("title_doc5").strip()

    return "unknown", ""

def _node_kind_and_position_tblr(m: re.Match) -> Tuple[int|None, int|None]:
    if m.group("title_paren2") is not None:
        return int(m.group("paren_pos_tb")), int(m.group("paren_pos_lr"))
    if m.group("title_bracket2") is not None:
        return int(m.group("bracket_pos_tb")), int(m.group("bracket_pos_lr"))
    if m.group("title_brace2") is not None:
        return int(m.group("brace_pos_tb")), int(m.group("brace_pos_lr"))
    if m.group("title_slash2") is not None:
        return int(m.group("slash_pos_tb")), int(m.group("slash_pos_lr"))
    if m.group("title_paren4") is not None:
        return int(m.group("paren_pos_tb2")), int(m.group("paren_pos_lr2"))
    if m.group("title_bracket4") is not None:
        return int(m.group("bracket_pos_tb2")), int(m.group("bracket_pos_lr2"))
    if m.group("title_brace4") is not None:
        return int(m.group("brace_pos_tb2")), int(m.group("brace_pos_lr2"))
    if m.group("title_slash4") is not None:
        return int(m.group("slash_pos_tb2")), int(m.group("slash_pos_lr2"))
    if m.group("title_cyl4") is not None:
        return int(m.group("cyl_pos_tb2")), int(m.group("cyl_pos_lr2"))
    if m.group("title_doc4") is not None:
        return int(m.group("doc_pos_tb2")), int(m.group("doc_pos_lr2"))
    return None, None

def _node_kind_and_position_xy(m: re.Match) -> Tuple[int|None, int|None]:
    if m.group("title_paren5") is not None:
        return int(m.group("paren_pos_x")), int(m.group("paren_pos_y"))
    if m.group("title_bracket5") is not None:
        return int(m.group("bracket_pos_x")), int(m.group("bracket_pos_y"))
    if m.group("title_brace5") is not None:
        return int(m.group("brace_pos_x")), int(m.group("brace_pos_y"))
    if m.group("title_slash5") is not None:
        return int(m.group("slash_pos_x")), int(m.group("slash_pos_y"))
    if m.group("title_cyl5") is not None:
        return int(m.group("cyl_pos_x")), int(m.group("cyl_pos_y"))
    if m.group("title_doc5") is not None:
        return int(m.group("doc_pos_x")), int(m.group("doc_pos_y"))
    return None, None

def convert_pos_to_xy(pos_tb: int|None, pos_lr: int|None, start_x: int, start_y: int) -> Tuple[int|None, int|None]:
    if pos_tb is None or pos_lr is None:
        x, y = None, None
    else:
        block_width = int(ct.NODE_DEFAULT_PARAMS["width"] + ct.CANVAS_PARAMS["grid_spacing"] * 4)
        block_height = int(ct.NODE_DEFAULT_PARAMS["height"] + ct.CANVAS_PARAMS["grid_spacing"])
        x = start_x + pos_lr * block_width
        y = start_y + pos_tb * block_height

    return x, y

def parse_mermaid_flowdata(text: str, canvas_width: int|None = None) -> Tuple[Dict[str, Node], List[Link]]:
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
            pos_x, pos_y = _node_kind_and_position_xy(nm)
            if pos_x is None or pos_y is None:
                pos_tb, pos_lr = _node_kind_and_position_tblr(nm)
                if pos_tb is not None and pos_lr is not None:
                    if canvas_width is None:
                        start_x = int(ct.CANVAS_PARAMS["grid_spacing"] * 20 + ct.NODE_DEFAULT_PARAMS["width"] / 2)
                    else:
                        start_x = int(canvas_width / 2)
                    start_y = int(ct.CANVAS_PARAMS["grid_spacing"] * 2 + ct.NODE_DEFAULT_PARAMS["height"] / 2)
                    pos_x, pos_y = convert_pos_to_xy(pos_tb, pos_lr, start_x=start_x, start_y=start_y)
            else:
                pos_tb, pos_lr = None, None
            nodes[node_id] = Node(node_id=node_id, kind=kind, title=title, raw=line, pos_tb=pos_tb, pos_lr=pos_lr, pos_x=pos_x, pos_y=pos_y)
            continue

        # 2) Link line? (contains -->)
        if "-->" in line or ".->" in line:
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

    node_pat = re.compile(r"\s*([A-Za-z][A-Za-z]*)\s*")
    edge_pat_elbow = re.compile(
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
    edge_pat_line = re.compile(
        r"""
        \s*
        (
            -\.->                        # dotted
          | -\.\.->                       # dotted
          | -\.\s*(?P<label>.*?)\s*\.->   # labeled
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
        em_elbow = edge_pat_elbow.match(s, i)
        em_line = edge_pat_line.match(s, i)
        if not em_elbow and not em_line:
            break
        elif em_elbow:
            label = em_elbow.group("label")
            edge_type = ct.EDGE_TYPE_ELBOW
        else:
            label = em_line.group("label")
            edge_type = ct.EDGE_TYPE_LINE
        label = label.strip() if label is not None else None
        if label is not None and len(label) > 3 and label.startswith('"') and label.endswith('"'):
            label = label[1:-1].strip()  # remove surrounding quotes if present
        i = em_elbow.end() if em_elbow else em_line.end()

        nm = node_pat.match(s, i)
        if not nm:
            break
        nxt = nm.group(1)
        i = nm.end()

        links.append(Link(src=cur, dst=nxt, label=label, edge_type=edge_type))
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
        out.append(f"node_id:{n.node_id}, kind:{n.kind}, title:{n.title}, pos_x:{n.pos_x}, pos_y:{n.pos_y}, pos_tb:{n.pos_tb}, pos_lr:{n.pos_lr}")
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

# 動作テスト用メイン
if __name__ == "__main__":
    sample = """```mermaid
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
    ```"""
    nodes, links = parse_mermaid_flowdata(sample)

    print("### Nodes (CSV lines)")
    for line in nodes_to_csv_lines(nodes):
        print(line)

    print("\n### Links (CSV lines)")
    for line in links_to_csv_lines(links):
        print(line)


    sample2 = """```mermaid
    flowchart TD
      A@{ shape: stadium, label: 開始, bx: 0, by: 0 }
      B@{ shape: rounded, label: "ツールの起動", bx: 0, by: 1 }
      C@{ shape: diamond, label: "新規作成or編集?", bx: 0, by: 2 }
      D@{ shape: rounded, label: "作図", bx: -1, by: 3 }
      E@{ shape: lean-r, label: "データ読込", bx: 1, by: 3 }
      F@{ shape: rounded, label: "編集", bx: 1, by: 4 }
      G@{ shape: lean-r, label: "画像出力", bx: 0, by: 5 }
      H@{ shape: rounded, label: "資料に画像を添付", bx: 0, by: 6 }
      I@{ shape: stadium, label: "終了", bx: 0, by: 7 }

      A --> B --> C -- "新規作成" --> D --> G --> H --> I
      C -- "編集" --> E --> F --> G
    ```"""
    nodes2, links2 = parse_mermaid_flowdata(sample2)

    print("### Nodes2 (CSV lines)")
    for line in nodes_to_csv_lines(nodes2):
        print(line)

    print("\n### Links2 (CSV lines)")
    for line in links_to_csv_lines(links2):
        print(line)


    sample3 = """```mermaid
flowchart TD
  A@{ shape: stadium, label: "開始", x: 600, y: 52 }
  B@{ shape: rounded, label: "ゲーム初期化", x: 600, y: 112 }
  C@{ shape: lean-r, label: "ブロック・パドル・ボール配置", x: 600, y: 172 }
  D@{ shape: rounded, label: "残機・スコア初期化", x: 600, y: 232 }
  E@{ shape: lean-r, label: "プレイヤー入力受付", x: 600, y: 292 }
  F@{ shape: rounded, label: "パドル移動処理", x: 600, y: 352 }
  G@{ shape: rounded, label: "ボール移動処理", x: 600, y: 412 }
  H@{ shape: diamond, label: "壁に衝突?", x: 600, y: 472 }
  I@{ shape: rounded, label: "ボール反射処理", x: 765, y: 472 }
  J@{ shape: diamond, label: "パドルに衝突?", x: 600, y: 562 }
  K@{ shape: rounded, label: "ボール反射処理", x: 765, y: 562 }
  L@{ shape: diamond, label: "ブロックに衝突?", x: 600, y: 637 }
  M@{ shape: rounded, label: "ブロック消去・スコア加算", x: 600, y: 697 }
  N@{ shape: rounded, label: "ボール反射処理", x: 600, y: 757 }
  O@{ shape: diamond, label: "全ブロック破壊?", x: 600, y: 817 }
  P@{ shape: lean-r, label: "ゲームクリア表示", x: 600, y: 877 }
  Q@{ shape: diamond, label: "ボール画面外?", x: 765, y: 862 }
  R@{ shape: rounded, label: "残機を減らす", x: 765, y: 922 }
  S@{ shape: diamond, label: "残機0?", x: 765, y: 982 }
  T@{ shape: lean-r, label: "ゲームオーバー表示", x: 675, y: 1027 }
  U@{ shape: rounded, label: "ボール再配置", x: 855, y: 1027 }
  V@{ shape: lean-r, label: "画面描画", x: 945, y: 1102 }
  W@{ shape: stadium, label: "終了", x: 600, y: 1102 }

  A -.-> B
  B -..-> C
  C --> D
  D --> E
  E --> F
  F --> G
  G --> H
  H -. "Yes" .-> I
  I --> J
  H -- "No" --> J
  J -- "Yes" --> K
  K --> L
  J -- "No" --> L
  L -- "Yes" --> M
  M --> N
  N --> O
  L -- "No" --> Q
  O -- "Yes" --> P
  P --> W
  O -- "No" --> Q
  Q -- "Yes" --> R
  R --> S
  Q -- "No" --> 22
  S -- "Yes" --> T
  T --> W
  S -- "No" --> U
  U --> V
  V --> E
```"""
    nodes3, links3 = parse_mermaid_flowdata(sample3)
    print("### Nodes3 (CSV lines)")
    for line in nodes_to_csv_lines(nodes3):
        print(line)

    print("\n### Links3 (CSV lines)")
    for line in links_to_csv_lines(links3):
        print(line)
