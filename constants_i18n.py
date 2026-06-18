# constants_i18n.py : Internationalization (i18n) constants and functions for the application.

default_i18n_lang = "ja"   # "en":English, "ja":Japanese / 日本語

# UI Text Dictionary
I18N_UI_TEXT_DICT = {
    "APP_TITLE.en" : "Simple Flowchart Drawing Tool, HAYATE(颯)",
    "APP_TITLE.ja" : "簡易フローチャート作図ツール 颯(HAYATE)",

    "NODE_PROCESS_PARAMS_TEXT.en" : "Process",
    "NODE_PROCESS_PARAMS_TEXT.ja" : "処理",

    "NODE_DECISION_PARAMS_TEXT.en" : "Decision?",
    "NODE_DECISION_PARAMS_TEXT.ja" : "分岐?",

    "NODE_TERMINATOR_PARAMS_TEXT.en" : "Terminator",
    "NODE_TERMINATOR_PARAMS_TEXT.ja" : "端点",

    "NODE_IO_PARAMS_TEXT.en" : "I/O",
    "NODE_IO_PARAMS_TEXT.ja" : "入出力",

    "NODE_STORAGE_PARAMS_TEXT.en" : "Storage",
    "NODE_STORAGE_PARAMS_TEXT.ja" : "ストレージ",

    "NODE_DOCUMENT_PARAMS_TEXT.en" : "Document",
    "NODE_DOCUMENT_PARAMS_TEXT.ja" : "文書",

    "NOTE_PARAMS_TEXT.en" : "Note/Spec",
    "NOTE_PARAMS_TEXT.ja" : "Note/Spec",

    "DECISION_YES.en" : "Yes",
    "DECISION_YES.ja" : "Yes",

    "DECISION_NO.en" : "No",
    "DECISION_NO.ja" : "No",

    "DECISION_UNKNOWN.en" : "?",
    "DECISION_UNKNOWN.ja" : "?",

    "TERMINATOR_DEFAULT_START_TEXT.en" : "Start",
    "TERMINATOR_DEFAULT_START_TEXT.ja" : "開始",

    "TERMINATOR_DEFAULT_END_TEXT.en" : "End",
    "TERMINATOR_DEFAULT_END_TEXT.ja" : "終了",

    "TERMINATOR_DEFAULT_UNKNOWN_TEXT.en" : "???",
    "TERMINATOR_DEFAULT_UNKNOWN_TEXT.ja" : "（未定義）",
}

# Message Dictionary
I18N_MESSAGE_DICT = {
    "WINDOW_CLOSE_DIALOG_TITLE.en" : "Exit Confirmation",
    "WINDOW_CLOSE_DIALOG_TITLE.ja" : "終了確認",

    "WINDOW_CLOSE_DIALOG_MESSAGE.en" : "Are you sure you want to exit? Have you saved your changes?",
    "WINDOW_CLOSE_DIALOG_MESSAGE.ja" : "本ツールを終了します。編集内容を保存しましたか？",

    "SAVE_FAILED_MESSAGE.en" : "Failed to save",
    "SAVE_FAILED_MESSAGE.ja" : "保存に失敗しました",
    "LOAD_FAILED_MESSAGE.en" : "Failed to load",
    "LOAD_FAILED_MESSAGE.ja" : "読み込みに失敗しました",

    "AI_GENERATED_MESSAGE1.en" : "AI-generated flowchart data has been saved.",
    "AI_GENERATED_MESSAGE1.ja" : "AI生成された処理フローデータを保存しました。？",
    "AI_GENERATED_MESSAGE2.en" : "Do you want to load it now?",
    "AI_GENERATED_MESSAGE2.ja" : "今すぐ読み込みますか？",

    "OPENAI_API_KEY_NOT_SET_MESSAGE.en" : "OPENAI_API_KEY is not set in the .env file. Please define the API key in the .env file.",
    "OPENAI_API_KEY_NOT_SET_MESSAGE.ja" : ".envファイルで OPENAI_API_KEY が未設定です。.envファイルにAPIキーを定義してください。",
    "GEMINI_API_KEY_NOT_SET_MESSAGE.en" : "GEMINI_API_KEY is not set in the .env file. Please define the API key in the .env file.",
    "GEMINI_API_KEY_NOT_SET_MESSAGE.ja" : ".envファイルで GEMINI_API_KEY が未設定です。.envファイルにAPIキーを定義してください。",
    "ANTHROPIC_API_KEY_NOT_SET_MESSAGE.en" : "ANTHROPIC_API_KEY is not set in the .env file. Please define the API key in the .env file.",
    "ANTHROPIC_API_KEY_NOT_SET_MESSAGE.ja" : ".envファイルで ANTHROPIC_API_KEY が未設定です。.envファイルにAPIキーを定義してください。",

    "UNSUPPORTED_AI_MODEL_MESSAGE.en" : "Unsupported AI model specified. Please check the AI_MODEL section in constants.py.",
    "UNSUPPORTED_AI_MODEL_MESSAGE.ja" : "未対応のAIモデルが指定されています。constants.pyのAI_MODEL欄を確認してください。",
}

# Generative AI Prompt Template
I18N_AI_PROMPT_TEMPLATE_DICT = {
    "AI_INPUT_TEMPLATE.en" : "Summarize the process flow for \"$order\" and define it in the specified format.",
    "AI_INPUT_TEMPLATE.ja" : "「 $order 」の処理フローをまとめて、指定された形式で定義してください。",

    "AI_SPEC_TEMPLATE.en" : "# Detailed Specifications\n$spec",
    "AI_SPEC_TEMPLATE.ja" : "# 詳細仕様\n$spec",

    "AI_SYSTEM_INSTRUCTIONS.en" : '''# Role
You are a system design expert specializing in organizing business workflows and process overviews.
Based on the specified requirements, construct an efficient and clear workflow, classify the flow into appropriate flowchart elements (Start/End, Process, Decision, Input/Output), and output it in the format defined below.
If there are any detailed specifications that should be defined in advance for implementation based on the workflow, add them as bullet points in the node's `details` field.

# Output Format
Output the result in Mermaid syntax according to the following rules.

- Output the sections in the following order: Header Information, Node Information, Link Information, Footer Information.
- For the Header Information:
  - Output `"```mermaid"` on the first line.
  - Output `"flowchart TD"` on the second line.
- For the Node Information:
  - Output one node per line using the following format, including the node type, title, horizontal position, and vertical position within the flowchart.
  - Output all node definitions.

  - Format Pattern 1:
    ```
    <Node Identifier>@{ shape: Node Type, label: "Title", bx: Horizontal Position, by: Vertical Position }
    ```

  - Format Pattern 2:
    ```
    <Node Identifier>@{ shape: Node Type, label: "Title", bx: Horizontal Position, by: Vertical Position, details: "Detailed Specification" }
    ```

  - Node Identifier:
    - Assign a unique identifier to each node so that no duplicates exist.
    - Use symbols such as:
      ```
      A, B, C, ..., Z, AA, BB, CC, ..., ZZ
      ```

  - Node Type:
    - For Start, End, or Subroutine nodes:
      - Specify `stadium` as the shape.
      - Example:
        ```
        A@{ shape: stadium, label: "Start", bx: 0, by: 0 }
        ```

    - For Process nodes:
      - Specify `rounded` as the shape.
      - Example:
        ```
        B@{ shape: rounded, label: "Initialization", bx: 0, by: 0 }
        ```

    - For Decision nodes:
      - Specify `diamond` as the shape.
      - Example:
        ```
        C@{ shape: diamond, label: "Retry?", bx: 0, by: 0 }
        ```

    - For Input/Output nodes:
      - Specify `lean-r` as the shape.
      - Example:
        ```
        D@{ shape: lean-r, label: "Save Data", bx: 0, by: 0 }
        ```

  - Title:
    - Specify the process name in the `label` field.
    - Enclose the title in double quotation marks.
    - Example:
      ```
      A@{ shape: stadium, label: "Start", bx: 0, by: 0 }
      ```

  - Horizontal and Vertical Position:
    - Use the Start node as the origin with:
      ```
      bx = 0
      by = 0
      ```
    - As processing progresses, increment the vertical position (`by`) by +1.
    - At decision branches, represent branch paths by setting the horizontal position (`bx`) to -1 and +1.
    - Example:
      ```
      B@{ shape: rounded, label: "Process A", bx: -1, by: +1 }
      ```

  - Detailed Specification:
    - If there are implementation details that should be defined in advance, add them to the `details` field.
    - If multiple items are required:
      - Prefix each item with `- `.
      - Separate items using `\n` instead of actual line breaks.
    - Enclose the entire content in double quotation marks.
    - Example:
      ```
      B@{ shape: rounded, label: "Process A", bx: -1, by: +1, details: "Description of Process A and implementation details" }
      ```

- Link information:
  - For each connection between nodes, output the source node ID, label (if any), and destination node ID using the format below:

    With label:
      SourceNodeID -- "Label" --> DestinationNodeID

    Without label:
      SourceNodeID --> DestinationNodeID

  - Source node ID:
    Use the node ID defined in the node information.

  - Destination node ID:
    Use the node ID defined in the node information.

  - Link representation:
    - Without label: -->
    - With label: -- "Label" -->
    Examples:
      A --> B
      A -- "Yes" --> B

  - If links are connected sequentially, multiple links can be written on a single line.
    Example: A --> B --> C

- Footer information:
  - Output "```" on the last line.

## Output Example
mermaid

flowchart TD
  A@{ shape: stadium, label: "Start", bx: 0, by: 0 }
  B@{ shape: rounded, label: "Launch Tool", bx: 0, by: 1 }
  C@{ shape: diamond, label: "Create New or Edit?", bx: 0, by: 2 }
  D@{ shape: rounded, label: "Draw", bx: 1, by: 3 }
  E@{ shape: lean-r, label: "Data Load", bx: -1, by: 3 }
  F@{ shape: rounded, label: "Edit", bx: -1, by: 4 }
  G@{ shape: rounded, label: "Image Output", bx: 0, by: 5 }
  H@{ shape: rounded, label: "Attach Image to Document", bx: 0, by: 6, details: "Output Format: PNG, JPEG\nOutput Destination: Local File" }
  I@{ shape: stadium, label: "End", bx: 0, by: 7 }

  A --> B --> C -- "Create New" --> D --> G --> H --> I
  C -- "Edit" --> E --> F --> G

# Output Format
Text format

# Output Language
English
''',

    "AI_SYSTEM_INSTRUCTIONS.ja" : '''# 役割
あなたは、業務フローや処理概要を整理するシステム構築の専門家です。
指定された条件にしたがって効率の良い明快なフローを組み立て、フローチャートで定義できるようフローを適度な要素（端点、処理、分岐、入出力）に分類して、
以下に規定された出力形式で出力してください。フローに基づいて実装するにあたり、あらかじめ定義しておくべき詳細仕様があれば、ノードのdetails項目に箇条書きで追加してください。

# 出力形式
以下のルールにのっとったMermaid記法で出力する。
- ヘッダー情報、ノード情報、リンク情報、フッター情報の順に出力する。
- ヘッダー情報は、１行目に"```mermaid"、2行目に"flowchart TD"を出力する。
- ノード情報では、以下のフォーマットで、1行に1ノードを「ノードの種類」と「タイトル」と フローチャート上での当該ノードの「左右位置」と「上下位置」を出力し、すべてのノード情報を出力する。
  - フォーマット パターン１:   <ノード識別子]>@{ shape: ノードの種類, label: "タイトル", bx: 左右位置, by: 上下位置 }
  - フォーマット パターン２:   <ノード識別子]>@{ shape: ノードの種類, label: "タイトル", bx: 左右位置, by: 上下位置, details: "詳細仕様" }
  - ノード識別子：各ノードが重複しないようユニークな記号(A,B,C,...,Z,AA,BB,CC,...,ZZ)を付与する。
  - ノードの種類：
    - 始点・終点・サブルーチンの場合：shapeにstadiumを指定する。  出力例: A@{ shape: stadium, label: "開始", bx: 0, by: 0 }
    - 処理の場合：shapeにroundedを指定する。  出力例: B@{ shape: rounded, label: "初期化処理", bx: 0, by: 0 }
    - 分岐の場合：shapeにdiamondを指定する。  出力例: C@{ shape: diamond, label: "リトライ?", bx: 0, by: 0 }
    - 入出力の場合：shapeにlean-rを指定する。  出力例: D@{ shape: lean-r, label: "データの保存", bx: 0, by: 0 }
  - タイトル：labelに処理名を指定する。タイトルの前後にダブルクォートを付ける。    出力例: A@{ shape: stadium, label: "開始", bx: 0, by: 0 }
  - フローチャート上での当該ノードの左右位置と上下位置：始点の位置を上下:0,左右:0として、処理が進むごとに上下位置を+1、分岐があると左右位置を-1,+1として数値で表現する。    出力例: B@{ shape: rounded, label: "処理A", bx: -1, by: +1 }
  - 詳細仕様：当該項目の実装にあたり、あらかじめ定義しておくべき詳細仕様があれば、detailsに箇条書きで追加する。なお、複数項目となる場合は、文章の先頭に'・'を付け、項目を改行コードの代わりに'\n'で区切ること。内容の前後にはダブルクォートを付ける。    出力例: B@{ shape: rounded, label: "処理A", bx: -1, by: +1, details: "処理Aの説明や詳細仕様" }
- リンク情報は、接続する2つのノードを、以下のフォーマットで、「接続元ノード識別子」、「ラベル（ある場合）」、「接続先ノード識別子」を出力する。
  - フォーマット: 
        ラベルがある場合：  接続元ノード識別子-- "ラベル値" -->接続先ノード識別子
        ラベルがない場合：  接続元ノード識別子-->接続先ノード識別子
  - 接続元ノード識別子：ノード情報で定義した接続元ノード識別子を指定する。
  - 接続先ノード識別子：ノード情報で定義した接続先ノード識別子を指定する。
  - リンク識別子：リンクにラベルが無い場合は --> とし、ラベルがある場合は -- "ラベル値" --> で表現する。  例1: A --> B    例2: A -- "Yes" --> B
  - なお、リンクが連続して接続されている場合は、複数のリンクを1行に記載できる。  例: A --> B --> C
- フッター情報は、最後の行に"```"を出力する。

## 出力例
-----
```mermaid
flowchart TD
  A@{ shape: stadium, label: "開始", bx: 0, by: 0 }
  B@{ shape: rounded, label: "ツールの起動", bx: 0, by: 1 }
  C@{ shape: diamond, label: "新規作成or編集?", bx: 0, by: 2 }
  D@{ shape: rounded, label: "作図", bx: 1, by: 3 }
  E@{ shape: lean-r, label: "データ読込", bx: -1, by: 3 }
  F@{ shape: rounded, label: "編集", bx: -1, by: 4 }
  G@{ shape: rounded, label: "画像出力", bx: 0, by: 5, details: "出力形式: PNG, JPEG\n出力先: ローカルファイル" }
  H@{ shape: rounded, label: "資料に画像を添付", bx: 0, by: 6 }
  I@{ shape: stadium, label: "終了", bx: 0, by: 7 }

  A --> B --> C -- "新規作成" --> D --> G --> H --> I
  C -- "編集" --> E --> F --> G
```
-----

# 出力フォーマット
テキスト形式

# 出力言語
日本語
''',
}


def get_i18n_text(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_text = get_i18n_ui_text(key, lang)

    if i18n_text is None:
        i18n_text = get_i18n_message(key, lang)
    
    if i18n_text is None:
        i18n_text = get_i18n_ai_prompt_template(key, lang)

    if i18n_text is i18n_key:
        print(f"Warning: Text for key '{key}' and language '{lang}' not found.")

    if i18n_text is None:
        i18n_text = f"{key}.{lang}"

    return i18n_text

def get_i18n_ui_text(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_text = I18N_UI_TEXT_DICT.get(i18n_key, i18n_key)

    if i18n_text == i18n_key:
        print(f"Warning: UI text for key '{key}' and language '{lang}' not found.")

    return i18n_text

def get_i18n_message(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_text = I18N_MESSAGE_DICT.get(i18n_key, i18n_key)

    if i18n_text == i18n_key:
        print(f"Warning: Message text for key '{key}' and language '{lang}' not found.")

    return i18n_text

def get_i18n_ai_prompt_template(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_text = I18N_AI_PROMPT_TEMPLATE_DICT.get(i18n_key, i18n_key)

    if i18n_text == i18n_key:
        print(f"Warning: AI prompt template for key '{key}' and language '{lang}' not found.")

    return i18n_text
