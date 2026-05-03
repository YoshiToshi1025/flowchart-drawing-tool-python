import tkinter
from tkinter import filedialog, messagebox
from typing import Dict

import constants as ct
from node import Node
from edge import Edge

MermaidStrIdList: list[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
              "AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ", "KK", "LL", "MM", "NN", "OO", "PP", "QQ", "RR", "SS", "TT", "UU", "VV", "WW", "XX", "YY", "ZZ",
              "AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL", "MMM", "NNN", "OOO", "PPP", "QQQ", "RRR", "SSS", "TTT", "UUU", "VVV", "WWW", "XXX", "YYY", "ZZZ"]

nodeIdDict: Dict[int, str] = {}

def save_data_to_mermaid_file(nodes: Dict[int, Node], edges: Dict[int, Edge]) -> None:

    # 処理前に、念のため、nodeIdDictを初期化する
    _init_nodeIdDict()

    # nodesデータとedgesデータから、マーメイド記法のデータを生成する
    mermaid_data : str = ""
    # マーメイド記法のヘッダーデータを生成する
    mermaid_header_data = _get_mermaid_header_data()

    # マーメイド記法のノードデータを生成する
    mermaid_node_data = _get_mermaid_node_data(nodes)

    # マーメイド記法のエッジデータを生成する
    mermaid_edge_data = _get_mermaid_edge_data(edges)

    # マーメイド記法のフッターデータを生成する
    mermaid_footer_data = _get_mermaid_footer_data()

    # マーメイド記法のデータを結合する
    mermaid_data = mermaid_header_data + mermaid_node_data + mermaid_edge_data + mermaid_footer_data

    # マーメイド記法のデータをファイルに保存する
    _save_to_mermaid_file(mermaid_data)

    # ファイル保存後に、nodeIdDictを初期化する
    _init_nodeIdDict()

def _get_mermaid_header_data() -> str:
    return "```mermaid\nflowchart TD\n"

def _get_mermaid_node_data(nodes: Dict[int, Node]) -> str:
    mermaid_node_data : str = ""
    for node_id, node in nodes.items():
        mermaid_str_id = _get_mermaid_str_id(node_id)
        text = node.text.replace("\n", "\\n") if node.text is not None else ""
        if node.type == ct.NODE_PROCESS_PARAMS["type"]:             # 処理
            mermaid_node_data += f'  {mermaid_str_id}@{{ shape: rounded, label: "{text}", x: {node.x}, y: {node.y} }}\n'
        elif node.type == ct.NODE_DECISION_PARAMS["type"]:          # 分岐
            mermaid_node_data += f'  {mermaid_str_id}@{{ shape: diamond, label: "{text}", x: {node.x}, y: {node.y} }}\n'
        elif node.type == ct.NODE_TERMINATOR_PARAMS["type"]:        # 端点
            mermaid_node_data += f'  {mermaid_str_id}@{{ shape: stadium, label: "{text}", x: {node.x}, y: {node.y} }}\n'
        elif node.type == ct.NODE_IO_PARAMS["type"]:                # 入出力
            mermaid_node_data += f'  {mermaid_str_id}@{{ shape: lean-r, label: "{text}", x: {node.x}, y: {node.y} }}\n'
        elif node.type == ct.NODE_STORAGE_PARAMS["type"]:           # ストレージ
            mermaid_node_data += f'  {mermaid_str_id}@{{ shape: cyl, label: "{text}", x: {node.x}, y: {node.y} }}\n'
        elif node.type == ct.NODE_DOCUMENT_PARAMS["type"]:          # ドキュメント
            mermaid_node_data += f'  {mermaid_str_id}@{{ shape: doc, label: "{text}", x: {node.x}, y: {node.y} }}\n'
        else:                                                       # その他（未定義）
            mermaid_node_data += f'  {mermaid_str_id}@{{ shape: rect, label: "{text}", x: {node.x}, y: {node.y} }}\n'
    mermaid_node_data += "\n"

    return mermaid_node_data

def _get_mermaid_edge_data(edges: Dict[int, Edge]) -> str:
    mermaid_edge_data : str = ""
    for edge_id, edge in edges.items():
        if edge.from_node_obj is not None and edge.to_node_obj is not None:
            from_mermaid_str_id = _get_mermaid_str_id(edge.from_node_obj.id)
            to_mermaid_str_id = _get_mermaid_str_id(edge.to_node_obj.id)

            if edge.edge_type == "elbow":    # エルボータイプの場合、実線を指定する
                if edge.label_text is not None and edge.label_text != "":
                        label_text = edge.label_text.replace("\n", "\\n")
                        mermaid_edge_data += f'  {from_mermaid_str_id} -- "{label_text}" --> {to_mermaid_str_id}\n'
                else:
                    mermaid_edge_data += f'  {from_mermaid_str_id} --> {to_mermaid_str_id}\n'
            else:
                if edge.label_text is not None and edge.label_text != "":
                        label_text = edge.label_text.replace("\n", "\\n")
                        mermaid_edge_data += f'  {from_mermaid_str_id} -. "{label_text}" .-> {to_mermaid_str_id}\n'
                else:
                    mermaid_edge_data += f'  {from_mermaid_str_id} -.-> {to_mermaid_str_id}\n'

    return mermaid_edge_data

def _get_mermaid_footer_data() -> str:
    return "```\n"

def _save_to_mermaid_file(mermaid_data: str) -> None:    
    # ファイルダイアログを表示して、保存先のファイルパスを取得する
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mmd",
        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(mermaid_data)
            messagebox.showinfo("Success", "Mermaid data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Mermaid data: {e}")

def _get_mermaid_str_id(node_id: int) -> str:
    # node_idをMermaidStrIdListの文字列に変換するための辞書を作成する
    nodeIdDictLen = len(nodeIdDict)
    if nodeIdDict.get(node_id) is None:
        nodeIdDict[node_id] = MermaidStrIdList[nodeIdDictLen]

    return nodeIdDict[node_id]

def _init_nodeIdDict():
    nodeIdDict.clear()
