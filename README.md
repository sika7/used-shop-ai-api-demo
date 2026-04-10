# 中古ショップ AI API - デプロイ & Claude接続ガイド

## 全体の流れ

```
main.py (このAPI) → Railway/Renderで公開 → HTTPSのURLが発行される
→ ClaudeアプリにMCP設定 → Claudeが在庫を検索できるようになる
```

---

## STEP 1: Railwayにデプロイ（無料・5分）

1. https://railway.app にGitHubでログイン
2. 「New Project」→「Deploy from GitHub repo」
3. このファイル一式をGitHubに上げてから接続
4. 環境変数に `START_COMMAND` = `uvicorn main:app --host 0.0.0.0 --port $PORT` を追加
5. デプロイ完了後、`https://xxxx.railway.app` のURLが発行される

### ローカルテスト（デプロイ前に確認）
```bash
pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000/docs で動作確認
```

---

## STEP 2: Claudeアプリ（デスクトップ版）にMCP接続

Claudeアプリの設定ファイル `claude_desktop_config.json` に追記：

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "used-shop-api": {
      "url": "https://あなたのURL.railway.app/mcp/call",
      "tools_url": "https://あなたのURL.railway.app/mcp/tools"
    }
  }
}
```

---

## STEP 3: Claudeアプリでデモ実行

Claudeアプリを再起動すると、以下のように話しかけるだけで動く：

**ユーザー：**「3万円以下でiPadを探して」

**Claude（自動でAPIを叩いて）：**
> 在庫を確認しました！以下の商品があります：
> - iPad Air 第4世代 ¥28,800（ハードオフ渋谷店・状態B）
> - iPad 第8世代 ¥19,800（オフハウス池袋店・状態B）

---

## APIエンドポイント一覧

| エンドポイント | 説明 |
|---|---|
| `GET /items/search` | 在庫検索（keyword, max_price, category等） |
| `GET /items/{id}` | 商品詳細 |
| `GET /categories` | カテゴリ一覧 |
| `GET /mcp/tools` | Claudeへのツール定義 |
| `POST /mcp/call` | Claude→APIのツール呼び出し |
| `GET /docs` | Swagger UI（ブラウザでAPIテスト可） |

---

## 企業提案でのデモの見せ方

1. スマホ or PCでClaudeアプリを開く
2. 「3万以下でギターある？」と話しかける
3. ClaudeがリアルタイムでAPIを叩いて答えを返す

**「AIが在庫を見ている」をそのまま見せられる**のがポイント。
