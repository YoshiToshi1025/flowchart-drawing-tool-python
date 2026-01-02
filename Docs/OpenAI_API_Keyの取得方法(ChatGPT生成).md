以下は、**新規ユーザーが OpenAI API Key を取得する手順**と、**実務で重要な注意点**をまとめたものです。
（Pythonやアプリ連携を前提にした内容も含めています）

---

## ① OpenAI API Key を取得する手順

### 1. OpenAI公式サイトにアクセス

* [https://platform.openai.com/](https://platform.openai.com/)

### 2. OpenAIアカウントを作成

* **Sign up** をクリック
* メールアドレス or Google / Microsoft / Apple アカウントで登録
* メール認証を完了

※ ChatGPT Plus を使っていても、**API利用は別扱い**です

---

### 3. ダッシュボードにログイン

* ログイン後、OpenAI Platform の **Dashboard** が表示される

---

### 4. API Keys 画面を開く

* 右上のプロフィールアイコン
  → **View API keys**
  → **Create new secret key**

---

### 5. API Key を生成・保存

* `sk-...` で始まるキーが発行される
* **この画面でしか全文表示されない**
* 必ず以下のどこかに安全に保存：

  * パスワードマネージャ
  * `.env` ファイル
  * Secret Manager（本番環境）

---

## ② 請求（Billing）の設定【重要】

APIを実際に使うには **支払い設定が必須** です。

### 手順

1. **Billing → Overview**
2. **Add payment method**
3. クレジットカード登録

### ポイント

* 初期は **従量課金（Pay-as-you-go）**
* 無料枠は基本的に **ほぼ無い / 非常に少ない**
* 使った分だけ課金される（トークン単位）

---

## ③ API Key 利用時の注意点（超重要）

### 🔐 1. API Keyは絶対に公開しない

以下は **NG**：

* GitHubに直接コミット
* JavaScriptのフロントエンドに直書き
* ブログやスクショに写す

✅ 正解：

```bash
# .env
OPENAI_API_KEY=sk-xxxxxxxx
```

```python
import os
api_key = os.getenv("OPENAI_API_KEY")
```

---

### 🔁 2. Keyは用途別に分ける

* 開発用
* 本番用
* テスト用

→ 漏洩時の被害を最小化できる

---

### 🔄 3. 定期的にローテーションする

* 使わなくなったKeyは **削除**
* 漏洩が疑われたら即失効 → 再発行

---

### 💰 4. 使用量と料金を必ず監視

* **Billing → Usage**
* 想定外の請求が起きやすい例：

  * 無限ループ
  * ログ出力しすぎ
  * temperature高＋長文出力

➡ 月額上限（Usage limit）を設定推奨

---

### 📏 5. モデルごとに料金が違う

* 高性能モデルほど **高コスト**
* 開発時は軽量モデルを使うのが安全
* 本番でのみ高性能モデルを使う、など切り分ける

---

## ④ よくある勘違い

| 勘違い                  | 実際          |
| -------------------- | ----------- |
| ChatGPT Plus加入＝API無料 | ❌ 別課金       |
| API Keyは1個で十分        | ❌ 用途別が安全    |
| 少し使うだけだから請求は微額       | ❌ バグで一気に増える |

---

## ⑤ 初心者向けベストプラクティス（まとめ）

* ✅ API Keyは `.env` 管理
* ✅ Usage limit を必ず設定
* ✅ 開発・本番でKey分離
* ✅ ログとトークン数を意識
* ✅ 使わないKeyは削除

---

