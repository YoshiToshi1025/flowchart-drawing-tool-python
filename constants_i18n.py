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

    "OPERATION_INFO_TEXT.en" : 
        "\n"
        "[Keyboard Shortcut Definitions]\n"
        " DEL/BS   : Delete selected node/edge/swimlane\n"
        " ESC      : Cancel selection\n"
        " Ctrl-a   : Select all nodes/swimlanes\n"
        " Ctrl-z   : Undo\n"
        " Ctrl-y   : Redo\n"
        " Ctrl-0~9 : Change selected node/swimlane fill color\n"
        " Ctrl-'-' : Reset selected node/swimlane fill color\n"
        " Ctrl-w   : Increase selected node/swimlane width\n"
        " Ctrl-W   : Decrease selected node/swimlane width\n"
        " Ctrl-h   : Increase selected node/swimlane height\n"
        " Ctrl-H   : Decrease selected node/swimlane height\n"
        "\n"
        "-------------------------------------------------------\n"
        "\n"
        "[Canvas Operations]\n"
        " Area Selection (Drag) : Select nodes/swimlanes within the area\n"
        " Mouse Wheel           : Rotate toolbar menu selection\n"
        " Drag with Mouse_Wheel_Button : Scroll canvas\n"
        " Right Button          : Show context menu\n"
        "\n"
        "[Swimlane Operations]\n"
        " Click Header/Footer         : Select swimlane\n"
        " Shift + Click Header/Footer : Add to selection\n"
        " Drag Header/Footer          : Move swimlane\n"
        " Shift + Mouse_Wheel on Header/Footer : Change swimlane width\n"
        " Ctrl + Mouse_Wheel on Header/Footer  : Change swimlane height\n"
        " Double-Click Header/Footer  : Edit header and footer text\n"
        " Ctrl + Drag Header/Footer   : Duplicate selected nodes/swimlanes\n"
        "\n"
        "[Node Operations]\n"
        " Click               : Select node\n"
        " Shift + Click       : Add to selection\n"
        " Drag                : Move selected node and related notes\n"
        " Double-Click        : Edit text\n"
        " Shift + Mouse_Wheel : Change selected node width\n"
        " Ctrl + Mouse_Wheel  : Change selected node height\n"
        " Ctrl + Shift + Mouse_Wheel  : Change node type\n"
        " Ctrl + Drag         : Duplicate selected nodes/swimlanes\n"
        " Double-Click Mouse_Wheel_Button : Show node notes\n"
        "\n"
        "[Edge Operations]\n"
        " Click               : Select edge\n"
        " Double-Click        : Edit label\n"
        " Ctrl + Mouse_Wheel  : Change connection points\n"
        " Shift + Mouse_Wheel : Change edge bend distance\n"
        " Ctrl + Shift+Mouse_Wheel : Change label position\n"
        "\n"
        "[Note Operations]\n"
        " Drag         : Move specified note\n"
        " Double-Click : Edit text\n"
        " Clear text   : Delete note field\n",

    "OPERATION_INFO_TEXT.ja" : 
        "\n"
        "[ショートカットキー定義]\n"
        " DEL/BS   : 選択中のノード/リンク/スイムレーンを削除\n"
        " ESC      : 選択をキャンセル\n"
        " Ctrl-a   : すべてのノード/スイムレーンを選択\n"
        " Ctrl-z   : 元に戻す(UNDO)\n"
        " Ctrl-y   : やり直し(REDO)\n"
        " Ctrl-0~9 : 選択中のノード/スイムレーンの塗りつぶし色を変更\n"
        " Ctrl-'-' : 選択中のノード/スイムレーンの塗りつぶし色をリセット\n"
        " Ctrl-w   : 選択中のノード/スイムレーンの幅を増加\n"
        " Ctrl-W   : 選択中のノード/スイムレーンの幅を減少\n"
        " Ctrl-h   : 選択中のノード/スイムレーンの高さを増加\n"
        " Ctrl-H   : 選択中のノード/スイムレーンの高さを減少\n"
        "\n"
        "-------------------------------------------------------\n"
        "\n"
        "[キャンバス操作]\n"
        " 範囲選択(ドラッグ)         : 範囲内のノード/スイムレーンを選択\n"
        " マウスホイール            : ツールバーのメニュー選択を回転\n"
        " マウスホイールボタンでドラッグ : キャンバスをスクロール\n"
        " 右ボタン                  : コンテキストメニューを表示\n"
        "\n"
        "[スイムレーン操作]\n"
        " ヘッダ/フッタを クリック       : スイムレーンを選択\n"
        " ヘッダ/フッタを Shift+クリック : スイムレーンを追加選択\n"
        " ヘッダ/フッタを ドラッグ       : スイムレーンを移動\n"
        " ヘッダ/フッタを Shift+マウスホイール : スイムレーンの幅を変更\n"
        " ヘッダ/フッタを Ctrl+マウスホイール  : スイムレーンの高さを変更\n"
        " ヘッダ/フッタを ダブルクリック  : ヘッダとフッタのテキストを編集\n"
        " ヘッダ/フッタを Ctrl+ドラッグ  : 選択中のノード/スイムレーンを複製\n"
        "\n"
        "[ノード操作]\n"
        " クリック             : 指定ノードを選択\n"
        " Shift+クリック       : 指定ノードを追加選択\n"
        " ドラッグ             : 選択中のノードと関連ノートを移動\n"
        " ダブルクリック        : テキストを編集\n"
        " Shift+マウスホイール : 指定ノードの幅を変更\n"
        " Ctrl+マウスホイール  : 指定ノードの高さを変更\n"
        " Ctrl+Shift+マウスホイール : 指定ノードの種類を変更\n"
        " Ctrl+ドラッグ        : 選択中のノード/スイムレーンを複製\n"
        " マウスホイールボタンをダブルクリック : ノードのノート欄を表示\n"
        "\n"
        "[リンク操作]\n"
        " クリック             : 指定リンクを選択\n"
        " ダブルクリック        : ラベルを編集\n"
        " Ctrl+マウスホイール  : 接続ポイントを変更\n"
        " Shift+マウスホイール : リンクの折り返し距離を変更\n"
        " Ctrl+Shift+マウスホイール : ラベルの位置を変更\n"
        "\n"
        "[ノート操作]\n"
        " ドラッグ         : 指定ノートを移動\n"
        " ダブルクリック    : テキストを編集\n"
        " テキストを空にする : ノート欄を削除\n",
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
    "MOONSHOT_API_KEY_NOT_SET_MESSAGE.en" : "MOONSHOT_API_KEY is not set in the .env file. Please define the API key in the .env file.",
    "MOONSHOT_API_KEY_NOT_SET_MESSAGE.ja" : ".envファイルで MOONSHOT_API_KEY が未設定です。.envファイルにAPIキーを定義してください。",
    "MOONSHOT_API_KEY_NOT_SET_MESSAGE.en" : "MOONSHOT_API_KEY is not set in the .env file. Please define the API key in the .env file.",
    "MOONSHOT_API_KEY_NOT_SET_MESSAGE.ja" : ".envファイルで MOONSHOT_API_KEY が未設定です。.envファイルにAPIキーを定義してください。",
    "SPACEXAI_API_KEY_NOT_SET_MESSAGE.en" : "XAI_API_KEY is not set in the .env file. Please define the API key in the .env file.",
    "SPACEXAI_API_KEY_NOT_SET_MESSAGE.ja" : ".envファイルで XAI_API_KEY が未設定です。.envファイルにAPIキーを定義してください。",
    "UNSLOTH_API_KEY_NOT_SET_MESSAGE.en" : "UNSLOTH_API_KEY is not set in the .env file. Please define the API key in the .env file.",
    "UNSLOTH_API_KEY_NOT_SET_MESSAGE.ja" : ".envファイルで UNSLOTH_API_KEY が未設定です。.envファイルにAPIキーを定義してください。",
    "UNSUPPORTED_AI_MODEL_MESSAGE.en" : "Unsupported AI model specified. Please check the AI_MODEL section in constants.py.",
    "UNSUPPORTED_AI_MODEL_MESSAGE.ja" : "未対応のAIモデルが指定されています。constants.pyのAI_MODEL欄を確認してください。",
}

I18N_KEY_MOUSE_TEXT_DICT = {
    "KEY_MOUSE_DEFINITIONS_TITLE.en" : "Key & Mouse Operations",
    "KEY_MOUSE_DEFINITIONS_TITLE.ja" : "キー＆マウス操作",

    "SHORTCUT_KEY_TITLE.en" : "Shortcut Keys",
    "SHORTCUT_KEY_TITLE.ja" : "ショートカットキー",
    "SHORTCUT_KEY_COLUMN_1_TITLE.en" : "Key",
    "SHORTCUT_KEY_COLUMN_1_TITLE.ja" : "キー",
    "SHORTCUT_KEY_COLUMN_2_TITLE.en" : "Definition",
    "SHORTCUT_KEY_COLUMN_2_TITLE.ja" : "定義内容",

    "MOUSE_ACTION_FOR_CANVAS_TITLE.en" : "Canvas",
    "MOUSE_ACTION_FOR_CANVAS_TITLE.ja" : "キャンバス",
    "MOUSE_ACTION_FOR_CANVAS_COLUMN_1_TITLE.en" : "Mouse Action",
    "MOUSE_ACTION_FOR_CANVAS_COLUMN_1_TITLE.ja" : "マウス操作",
    "MOUSE_ACTION_FOR_CANVAS_COLUMN_2_TITLE.en" : "Definition",
    "MOUSE_ACTION_FOR_CANVAS_COLUMN_2_TITLE.ja" : "定義内容",

    "MOUSE_ACTION_FOR_SWIMLANE_TITLE.en" : "Swimlane",
    "MOUSE_ACTION_FOR_SWIMLANE_TITLE.ja" : "スイムレーン",
    "MOUSE_ACTION_FOR_SWIMLANE_COLUMN_1_TITLE.en" : "Mouse Action",
    "MOUSE_ACTION_FOR_SWIMLANE_COLUMN_1_TITLE.ja" : "マウス操作",
    "MOUSE_ACTION_FOR_SWIMLANE_COLUMN_2_TITLE.en" : "Definition",
    "MOUSE_ACTION_FOR_SWIMLANE_COLUMN_2_TITLE.ja" : "定義内容",

    "MOUSE_ACTION_FOR_NODE_TITLE.en" : "Node",
    "MOUSE_ACTION_FOR_NODE_TITLE.ja" : "ノード",
    "MOUSE_ACTION_FOR_NODE_COLUMN_1_TITLE.en" : "Mouse Action",
    "MOUSE_ACTION_FOR_NODE_COLUMN_1_TITLE.ja" : "マウス操作",
    "MOUSE_ACTION_FOR_NODE_COLUMN_2_TITLE.en" : "Definition",
    "MOUSE_ACTION_FOR_NODE_COLUMN_2_TITLE.ja" : "定義内容",

    "MOUSE_ACTION_FOR_LINK_TITLE.en" : "Link",
    "MOUSE_ACTION_FOR_LINK_TITLE.ja" : "リンク",
    "MOUSE_ACTION_FOR_LINK_COLUMN_1_TITLE.en" : "Mouse Action",
    "MOUSE_ACTION_FOR_LINK_COLUMN_1_TITLE.ja" : "マウス操作",
    "MOUSE_ACTION_FOR_LINK_COLUMN_2_TITLE.en" : "Definition",
    "MOUSE_ACTION_FOR_LINK_COLUMN_2_TITLE.ja" : "定義内容",

    "MOUSE_ACTION_FOR_NOTE_TITLE.en" : "Note",
    "MOUSE_ACTION_FOR_NOTE_TITLE.ja" : "ノート",
    "MOUSE_ACTION_FOR_NOTE_COLUMN_1_TITLE.en" : "Mouse Action",
    "MOUSE_ACTION_FOR_NOTE_COLUMN_1_TITLE.ja" : "マウス操作",
    "MOUSE_ACTION_FOR_NOTE_COLUMN_2_TITLE.en" : "Definition",
    "MOUSE_ACTION_FOR_NOTE_COLUMN_2_TITLE.ja" : "定義内容",
}

I18N_KEY_MOUSE_LIST_DICT = {
    "SHORTCUT_KEY_LIST.ja" : [
            ("DEL/BS", "選択中のノード/リンク/スイムレーンを削除"),
            ("ESC", "選択をキャンセル"),
            ("Ctrl-a", "すべてのノード/スイムレーンを選択"),
            ("Ctrl-z", "元に戻す(UNDO)"),
            ("Ctrl-y", "やり直し(REDO)"),
            ("Ctrl-0~9", "選択中のノード/スイムレーンの塗りつぶし色を変更"),
            ("Ctrl-'-'", "選択中のノード/スイムレーンの塗りつぶし色をリセット"),
            ("Ctrl-w", "選択中のノード/スイムレーンの幅を増加"),
            ("Ctrl-W", "選択中のノード/スイムレーンの幅を減少"),
            ("Ctrl-h", "選択中のノード/スイムレーンの高さを増加"),
            ("Ctrl-H", "選択中のノード/スイムレーンの高さを減少"),
        ],
    "SHORTCUT_KEY_LIST.en" : [
            ("DEL/BS", "Delete the selected node/link/swimlane"),
            ("ESC", "Cancel selection"),
            ("Ctrl-a", "Select all nodes/swimlanes"),
            ("Ctrl-z", "Undo the previous action"),
            ("Ctrl-y", "Redo the previously undone action"),
            ("Ctrl-0~9", "Change the fill color of the selected node/swimlane"),
            ("Ctrl-'-'", "Reset the fill color of the selected node/swimlane"),
            ("Ctrl-w", "Increase the width of the selected node/swimlane"),
            ("Ctrl-W", "Decrease the width of the selected node/swimlane"),
            ("Ctrl-h", "Increase the height of the selected node/swimlane"),
            ("Ctrl-H", "Decrease the height of the selected node/swimlane"),
        ],
    "MOUSE_ACTION_FOR_CANVAS_LIST.ja" : [
            ("範囲選択(ドラッグ)", "範囲内のノード/スイムレーンを選択"),
            ("マウスホイール", "ツールバーのメニュー選択を回転"),
            ("マウスホイールボタンでドラッグ", "キャンバスをスクロール"),
            ("右ボタン", "コンテキストメニューを表示"),
        ],
    "MOUSE_ACTION_FOR_CANVAS_LIST.en" : [
            ("Range Select (Drag)", "Select nodes/swimlanes within the area"),
            ("Mouse Wheel", "Rotate the toolbar menu selection"),
            ("Drag with Mouse Wheel Button", "Scroll the canvas"),
            ("Right Button", "Show context menu"),
        ],
    "MOUSE_ACTION_FOR_SWIMLANE_LIST.ja" : [
            ("ヘッダ/フッタを クリック", "スイムレーンを選択"),
            ("ヘッダ/フッタを Shift+クリック", "スイムレーンを追加選択"),
            ("ヘッダ/フッタを ドラッグ", "スイムレーンを移動"),
            ("ヘッダ/フッタを Shift+マウスホイール", "スイムレーンの幅を変更"),
            ("ヘッダ/フッタを Ctrl+マウスホイール", "スイムレーンの高さを変更"),
            ("ヘッダ/フッタを ダブルクリック", "ヘッダとフッタのテキストを編集"),
            ("ヘッダ/フッタを Ctrl+ドラッグ", "選択中のノード/スイムレーンを複製"),
        ],
    "MOUSE_ACTION_FOR_SWIMLANE_LIST.en" : [
            ("Click Header/Footer", "Select swimlane"),
            ("Shift + Click Header/Footer", "Add to selection"),
            ("Drag Header/Footer", "Move swimlane"),
            ("Shift + Mouse Wheel on Header/Footer", "Change swimlane width"),
            ("Ctrl + Mouse Wheel on Header/Footer", "Change swimlane height"),
            ("Double-Click Header/Footer", "Edit header and footer text"),
            ("Ctrl + Drag Header/Footer", "Duplicate selected nodes/swimlanes"),
        ],
    "MOUSE_ACTION_FOR_NODE_LIST.ja" : [
            ("クリック", "指定ノードを選択"),
            ("Shift+クリック", "指定ノードを追加選択"),
            ("ドラッグ", "選択中のノードと関連ノートを移動"),
            ("ダブルクリック", "テキストを編集"),
            ("Shift+マウスホイール", "指定ノードの幅を変更"),
            ("Ctrl+マウスホイール", "指定ノードの高さを変更"),
            ("Ctrl+Shift+マウスホイール", "指定ノードの種類を変更"),
            ("Ctrl+ドラッグ", "選択中のノード/スイムレーンを複製"),
            ("マウスホイールボタンをダブルクリック", "ノードのノート欄を表示"),
        ],
    "MOUSE_ACTION_FOR_NODE_LIST.en" : [
            ("Click", "Select the specified node"),
            ("Shift + Click", "Add to selection"),
            ("Drag", "Move selected node and related notes"),
            ("Double-Click", "Edit text"),
            ("Shift + Mouse Wheel", "Change selected node width"),
            ("Ctrl + Mouse Wheel", "Change selected node height"),
            ("Ctrl + Shift + Mouse Wheel", "Change node type"),
            ("Ctrl + Drag", "Duplicate selected nodes/swimlanes"),
            ("Double-Click Mouse Wheel Button", "Show node notes"),
        ],
    "MOUSE_ACTION_FOR_LINK_LIST.ja" : [
            ("クリック", "指定リンクを選択"),
            ("ダブルクリック", "ラベルを編集"),
            ("Ctrl+マウスホイール", "接続ポイントを変更"),
            ("Shift+マウスホイール", "リンクの折り返し距離を変更"),
            ("Ctrl+Shift+マウスホイール", "ラベルの位置を変更"),
        ],
    "MOUSE_ACTION_FOR_LINK_LIST.en" : [
            ("Click", "Select the specified link"),
            ("Double-Click", "Edit the label"),
            ("Ctrl+Mouse Wheel", "Change the connection point"),
            ("Shift+Mouse Wheel", "Change the link wrap distance"),
            ("Ctrl+Shift+Mouse Wheel", "Change the label position"),
        ],
    "MOUSE_ACTION_FOR_NOTE_LIST.ja" : [
            ("ドラッグ", "指定ノートを移動"),
            ("ダブルクリック", "テキストを編集"),
            ("テキストを空にする", "ノート欄を削除"),
        ],
    "MOUSE_ACTION_FOR_NOTE_LIST.en" : [
            ("Drag", "Move the specified note"),
            ("Double-Click", "Edit text"),
            ("Clear text", "Delete the note field"),
        ],
}


I18N_HELP_TEXT_DICT = {
    "BASIC_HELP_TITLE.en" : "Basic Guide",
    "BASIC_HELP_TITLE.ja" : "簡易ガイド",

    "BASIC_HELP_TEXT.en" : """Basic Flowchart Drawing Operations

# Placing Nodes
(1) Select the node type you want to place from the toolbar.
(2) Click the desired position on the canvas.
→ A node will be created at the specified position.
(3) Drag the node to fine-tune its position.
(4) Double-click the node to enter text.

# Connecting Links
(1) Select Link from the toolbar.
(2) Click and hold the source node, drag to the destination node, and release the mouse button.
→ A link will be created between the two nodes.
(3) To change the link connection path (routing), use Ctrl+Wheel.
(4) To add a label to a link, double-click the link and enter text.

# Moving Nodes
(1) Select the Select icon from the toolbar.
(2) Select the nodes you want to move using the mouse.
・Click: Select a node
・Shift+Click: Add a node to the current selection
・Drag on the canvas to select an area: Select all nodes within the specified area
(3) Click one of the selected nodes and drag it to the desired position.
→ All selected nodes will move together to the specified position.

# Deleting Nodes / UNDO / REDO
・Click the Delete icon
→ Deletes the currently selected nodes.
・Click the Undo icon
→ Undoes the previous editing operation.
・Click the Redo icon
→ Redoes the previously undone operation.

# Editing Nodes
・Double-click a node
→ Edit the node text.
・Select a node and press Ctrl+w/W/h/H
→ Increase or decrease the node width/height.
・Select a node and use Ctrl+Wheel
→ Change the node type.
・Select a node and press Ctrl+0~9
→ Change the node fill color.

# Saving / Loading a Flowchart
・Click the Save JSON icon
→ Saves the current flowchart data in JSON format.
・Click the Load JSON icon
→ Loads saved flowchart data onto the canvas.
""",
    "BASIC_HELP_TEXT.ja" :"""フローチャート作図の基本操作

■ノードの配置
 (1)配置したいノードをツールバーで選択
 (2)キャンバス内で、配置したい位置をクリック
        → 指定位置にノードが作図される
 (3)ノードのドラッグ操作で位置を微調整
 (4)ノードをダブルクリックしてテキストを入力

■リンクの接続
 (1)ツールバーでリンクを選択
 (2)接続元のノードをクリックしたまま、接続先のノードで離す
        → 2つのノード間のリンクが作図される
 (3)リンクの接続位置（回り込み）の変更は、Ctrl+Wheelで調整できる
 (4)リンクにラベルを付けるには、リンクをダブルクリックして文字入力

■ノードの移動
 (1)ツールバーで Select アイコンを選択
 (2)移動したいノードをマウス操作で選択
    ・クリック：ノード選択
    ・Shift+クリック：追加選択
    ・キャンバスをドラッグ操作で範囲選択：指定範囲内のノードを選択
 (3)選択したノードの１つをクリックして、ドラッグ操作で移動先を指定
        → 選択中のノードすべてが指定位置に移動される

■ノードの削除/UNDO/REDO
 ・Delete アイコンをクリック → 選択中のノードが削除される
 ・Undo アイコンをクリック → 編集操作が１回戻る
 ・Redo アイコンをクリック → 取消操作が１回戻る

■ノードの編集
 ・ノードをダブルクリック → テキストの編集ができる
 ・ノードを選択して Ctrl+w/W/h/H → ノードの幅/高さを増減できる
 ・ノードを選択して Ctrl+Wheel → ノードの種類を変更できる
 ・ノードを選択して Ctrl-0～9 → ノードの塗りつぶし色を変更できる

■作図したフローチャートの保存/読込
 ・Save JSON アイコンを選択クリック
        → 作図中のデータがJSON形式で保存される
 ・Load JSON アイコンを選択クリック
        → 保存済のフローチャートデータがキャンバスに読み込まれる
""",
}

I18N_RELEASE_NOTE_DICT = {
  "RELEASE_NOTE_TITLE.en" : "Release Notes",
  "RELEASE_NOTE_TITLE.ja" : "リリースノート",

  "RELEASE_NOTE_TEXT.en" : """Release Notes

[ 2026/09/09 ]
- Bug fixes
  - Adjusted tab display in the slide panel on macOS
  - Fixed an issue where the display could become distorted at application startup
  - Fixed an issue where mouse-based width adjustment did not work for multiple selected nodes

[ 2026/09/07 ]
- Added right-side slide panels for key bindings, a quick operation guide, and release notes
- Made the AI integration slide panel resizable
- Confirmed compatibility with the latest AI models (GPT-6 Astra, Claude Fable 5.1, Gemini 3.8 Flash)
- Fixed display issues caused by node resizing
- Fixed an issue when loading node information in the AI integration feature

[ 2026/08/25 ]
- Added support for connecting to Unsloth through the generative AI integration.
- Added support for changing node width and height using mouse operations (Shift/Ctrl + Wheel) or keyboard shortcuts (Ctrl + w/W/h/H).
- Changed the keyboard shortcut for changing the node type from Ctrl + Wheel to Ctrl + Shift + Wheel due to the above feature enhancement.

[ 2026/08/15 ]
- Added support for new generative AI models (Grok 4.6, Gemini 3.7 Flash) in the generative AI integration.
- Added support for changing the node type using Ctrl + Wheel.
- Reorganized the list of keyboard shortcuts and mouse operations displayed on the initial screen.

[ 2026/07/27 ]
- Added support for new generative AI models (Gemini 3.6 Flash, Claude Opus 5, Kimi K3) in the generative AI integration.
- Fixed an issue when loading generative AI data, including support for escape characters in the note field.

[ 2026/07/11 ]
- Added support for new generative AI models (GPT 5.6 Sol/Terra/Luna, Claude Fable 5) in the generative AI integration.
- Added support for connecting to LM Studio through the generative AI integration.

[ 2026/07/04 ]
- Fixed an issue with Backspace handling during text editing, where deleting text could also delete elements at the same time.

[ 2026/06/28 ]
- Added support for duplicating selected nodes/swimlanes and links between selected elements using Ctrl + Drag.
- Improved usability on macOS:
  - Added support for deleting nodes and other elements using the Backspace key in addition to the Delete key.
  - Added support for specifying line breaks with \n during text editing.
- Fixed an issue with swimlane movement.
""",
  "RELEASE_NOTE_TEXT.ja" : """リリースノート

[ 2026/09/09 ]
・不具合対応
  ・macOSでのスライドパネル内のタブ表示の調整、
  ・アプリ起動時に表示が乱れることがある件への対応
  ・複数選択したノードに対するマウス操作による幅調整が効かない件への対応

[ 2026/09/07 ]
・キー定義、簡易操作ガイド、リリースノートを、右スライドで表示可能に
・生成AI連携用スライドの幅を可変に
・生成AI連携機能における最新生成AI(gpt-6-astra, claude-fable-5-1, gemini-3.8-flash)の動作確認
・ノードのサイズ変更に伴う表示不具合への対応
・生成AI連携でのノード情報読み込み不具合への対応

[ 2026/08/25 ]
・生成AI連携機能で、Unslothとの接続に対応
・マウス操作(Shift/Ctrl+Wheel)またはキー操作(Ctrl-w/W/h/H)でノードの幅と高さの変更を可能に
・上記機能拡張に伴い、ノードの種類変更のキー割当を変更（Ctrl+Wheel → Ctrl+Shift+Wheel）

[ 2026/08/15 ]
・生成AI連携機能で、新しい生成AIへの対応(Grok 4.6, Gemini 3.7 Flash)
・Ctrl+Wheel操作で、ノードの種類変更に対応
・初期画面に表示するショートカットキーとマウス操作の定義一覧の表示内容を整理

[ 2026/07/27 ]
・生成AI連携機能で、新しい生成AIへの対応(Gemini 3.6 Flash, Claude Opus 5, Kimi K3)
・生成AIデータ読み込み時の不具合に対応（note欄でのエスケープ文字の読込対応）

[ 2026/07/11 ]
・生成AI連携機能で、新しい生成AIへの対応(GPT 5.6 Sol/Terra/Luna, Claude Fable 5)
・生成AI連携機能で、LM Studioとの接続対応

[ 2026/07/04 ]
・文字列編集時のBackSpace処理の不具合対応(文字列削除時に同時に要素などが削除されていた事象に対応)

[ 2026/06/28 ]
・Ctrl+Drag操作で、選択中のノード/スイムレーンと選択中要素間のリンクの複製に対応
・macOSでの操作の改善
  ・DeleteキーだけでなくBackSpaceキーでもノードなどの削除を可能に
  ・テキスト編集で ￥n でも改行指定を可能に
・不具合対応（スイムレーンの移動処理）
""",
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

def get_i18n_key_mouse_text(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_text = I18N_KEY_MOUSE_TEXT_DICT.get(i18n_key, i18n_key)

    if i18n_text == i18n_key:
        print(f"Warning: Key/mouse text for key '{key}' and language '{lang}' not found.")

    return i18n_text

def get_i18n_key_mouse_list(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_list = I18N_KEY_MOUSE_LIST_DICT.get(i18n_key, i18n_key)

    if i18n_list == i18n_key:
        print(f"Warning: Key/mouse list for key '{key}' and language '{lang}' not found.")

    return i18n_list

def get_i18n_help_text(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_text = I18N_HELP_TEXT_DICT.get(i18n_key, i18n_key)

    if i18n_text == i18n_key:
        print(f"Warning: Help text for key '{key}' and language '{lang}' not found.")

    return i18n_text

def get_i18n_release_note(key, lang=default_i18n_lang):
    if key is None:
        return None
    if lang is None:
        lang=default_i18n_lang

    i18n_key = f"{key}.{lang}"
    i18n_text = I18N_RELEASE_NOTE_DICT.get(i18n_key, i18n_key)

    if i18n_text == i18n_key:
        print(f"Warning: Release note for key '{key}' and language '{lang}' not found.")

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
