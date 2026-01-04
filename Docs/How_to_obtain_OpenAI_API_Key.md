Below is a summary of the steps for **new users to obtain an OpenAI API Key**, along with **important practical precautions**.
(This also includes content assuming usage with Python or application integration.)

---

## ① Steps to Obtain an OpenAI API Key

1. **Access the official OpenAI website**
   [https://platform.openai.com/](https://platform.openai.com/)

2. **Create an OpenAI account**

   * Click **Sign up**
   * Register using an email address or a Google / Microsoft / Apple account
   * Complete email verification
   * *Note: Even if you are using ChatGPT Plus, API usage is handled separately.*

3. **Log in to the Dashboard**

   * After logging in, the **OpenAI Platform Dashboard** will be displayed.

4. **Open the API Keys page**

   * Top-right profile icon → **View API keys** → **Create new secret key**

5. **Generate and save the API Key**

   * A key starting with `sk-...` will be issued.
   * **The full key is displayed only once on this screen.**

   Be sure to securely store it in one of the following:

   * A password manager
   * A `.env` file
   * A Secret Manager (for production environments)

---

## ② Billing Setup 【Important】

To actually use the API, **payment setup is required**.

### Steps

* **Billing → Overview**
* **Add payment method**
* Register a credit card

### Key Points

* Billing is **pay-as-you-go** by default
* The free tier is **very limited or nearly nonexistent**
* Charges are based on usage (per token)

---

## ③ Important Notes When Using an API Key (Critical)

### 🔐 1. Never expose your API Key

The following are **NOT allowed**:

* Committing it directly to GitHub
* Hardcoding it in frontend JavaScript
* Showing it in blogs or screenshots

✅ Correct approach:

```env
# .env
OPENAI_API_KEY=sk-xxxxxxxx
```

```python
import os
api_key = os.getenv("OPENAI_API_KEY")
```

---

### 🔁 2. Separate keys by purpose

* Development
* Production
* Testing

→ This minimizes damage in case of a leak.

---

### 🔄 3. Rotate keys regularly

* Delete keys that are no longer used
* If leakage is suspected, revoke immediately and reissue

---

### 💰 4. Always monitor usage and costs

* **Billing → Usage**

Common causes of unexpected charges:

* Infinite loops
* Excessive logging
* High temperature + long outputs

➡ It is strongly recommended to set a **monthly usage limit**.

---

### 📏 5. Pricing differs by model

* Higher-performance models are more expensive
* Use lightweight models during development
* Use high-performance models only in production, as needed

---

## ④ Common Misconceptions

| Misconception                        | Reality                        |
| ------------------------------------ | ------------------------------ |
| ChatGPT Plus includes free API usage | ❌ Separate billing             |
| One API Key is enough                | ❌ Safer to separate by use     |
| Small usage won’t cost much          | ❌ Bugs can cause sudden spikes |

---

## ⑤ Beginner Best Practices (Summary)

* ✅ Manage API Keys with `.env` files
* ✅ Always set a usage limit
* ✅ Separate development and production keys
* ✅ Be mindful of logs and token usage
* ✅ Delete unused API Keys
