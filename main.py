# -*- coding: utf-8 -*-

import os
os.environ["MCP_ALLOWED_HOSTS"] = os.environ.get(
    "MCP_ALLOWED_HOSTS",
    "used-shop-ai-api-demo-production.up.railway.app"
)

"""
中古ショップ MCPサーバー
FastMCP (公式SDKのSSEトランスポート) でRailwayにデプロイ
Claudeアプリ → mcp-remote → このサーバー の構成で動く
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("中古ショップ AI検索")

# ── 在庫データ ─────────────────────────────────────────────────────
INVENTORY = [
    # ─ スマートフォン（通常中古）
    {"id": 1,  "name": "Apple iPhone 13 128GB ミッドナイト",         "price": 52000, "store": "ハードオフ 新宿店",   "condition": "中古A",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "スマートフォン", "brand": "Apple",  "notes": "SIMフリー・バッテリー91%"},
    {"id": 2,  "name": "Apple iPhone 12 mini 64GB ブラック",          "price": 24800, "store": "ハードオフ 渋谷店",   "condition": "中古B",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "スマートフォン", "brand": "Apple",  "notes": "SIMフリー・バッテリー85%"},
    {"id": 3,  "name": "Apple iPhone SE 第3世代 64GB スターライト",   "price": 29800, "store": "ゲオ 渋谷店",         "condition": "中古A",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "スマートフォン", "brand": "Apple",  "notes": "SIMフリー・付属品完備"},
    # ─ スマートフォン（ジャンク）
    {"id": 4,  "name": "Apple iPhone 12 mini 64GB ホワイト",          "price": 8800,  "store": "ハードオフ 渋谷店",   "condition": "ジャンク", "junk": True,  "working_parts": ["カメラ", "バッテリー", "スピーカー"], "broken_parts": ["画面割れ", "タッチ不良"],     "category": "スマートフォン", "brand": "Apple",  "notes": "画面割れ・タッチ不良。カメラ・バッテリー・スピーカー動作確認済み"},
    {"id": 5,  "name": "Apple iPhone 12 mini 128GB ブラック",         "price": 12000, "store": "ハードオフ 吉祥寺店", "condition": "ジャンク", "junk": True,  "working_parts": ["カメラ", "画面", "タッチ", "充電"],   "broken_parts": ["充電不良"],                   "category": "スマートフォン", "brand": "Apple",  "notes": "充電コネクタ不良。画面・タッチ・カメラは正常動作"},
    {"id": 6,  "name": "Apple iPhone 12 64GB レッド",                 "price": 7500,  "store": "オフハウス 池袋店",   "condition": "ジャンク", "junk": True,  "working_parts": ["カメラ", "タッチ", "充電"],           "broken_parts": ["液晶不良（バックライト弱）"], "category": "スマートフォン", "brand": "Apple",  "notes": "バックライト弱め。カメラ・タッチ・充電は正常"},
    {"id": 7,  "name": "Apple iPhone 11 128GB ブラック",              "price": 6800,  "store": "ハードオフ 新宿店",   "condition": "ジャンク", "junk": True,  "working_parts": ["画面", "タッチ", "充電", "スピーカー"],"broken_parts": ["カメラ不良（AF不可）"],       "category": "スマートフォン", "brand": "Apple",  "notes": "カメラのオートフォーカス不良。画面・タッチ・充電は正常"},
    {"id": 8,  "name": "SONY Xperia 5 IV",                            "price": 11000, "store": "ハードオフ 渋谷店",   "condition": "ジャンク", "junk": True,  "working_parts": ["カメラ", "画面", "充電"],             "broken_parts": ["SIM認識不良"],               "category": "スマートフォン", "brand": "SONY",   "notes": "SIMスロット認識不良。カメラ・画面・充電は正常"},
    # ─ タブレット
    {"id": 9,  "name": "Apple iPad Air 第4世代 64GB Wi-Fi",           "price": 28800, "store": "ハードオフ 渋谷店",   "condition": "中古B",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "タブレット",     "brand": "Apple",  "notes": ""},
    {"id": 10, "name": "Apple iPad Pro 11インチ 第2世代 128GB",        "price": 38000, "store": "ハードオフ 新宿店",   "condition": "中古A",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "タブレット",     "brand": "Apple",  "notes": ""},
    # ─ 楽器
    {"id": 11, "name": "YAMAHA アコースティックギター FG820",          "price": 24000, "store": "ハードオフ 渋谷店",   "condition": "中古B",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "楽器",           "brand": "YAMAHA", "notes": ""},
    {"id": 12, "name": "Fender Stratocaster エレキギター（メキシコ）", "price": 55000, "store": "ハードオフ 吉祥寺店", "condition": "中古A",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "楽器",           "brand": "Fender", "notes": ""},
    # ─ オーディオ
    {"id": 13, "name": "SONY WH-1000XM4 ヘッドフォン",                "price": 18500, "store": "ハードオフ 新宿店",   "condition": "中古A",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "オーディオ",     "brand": "SONY",   "notes": ""},
    {"id": 14, "name": "Marantz プリメインアンプ PM6006",              "price": 32000, "store": "ハードオフ 吉祥寺店", "condition": "中古B",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "オーディオ",     "brand": "Marantz","notes": ""},
    # ─ PC
    {"id": 15, "name": "Apple MacBook Air M1 8GB 256GB",              "price": 72000, "store": "ハードオフ 新宿店",   "condition": "中古A",   "junk": False, "working_parts": [],                                     "broken_parts": [],                            "category": "PC",             "brand": "Apple",  "notes": ""},
]


# ── MCPツール定義 ──────────────────────────────────────────────────

@mcp.tool()
def search_used_items(
    keyword: Optional[str] = None,
    max_price: Optional[int] = None,
    min_price: Optional[int] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    junk_only: Optional[bool] = None,
    working_parts: Optional[str] = None,
    broken_parts: Optional[str] = None,
) -> str:
    """
    中古ショップの在庫を検索します。
    ユーザーの自然な発話を解釈し、適切なパラメータに変換して呼んでください。

    【変換例】
    「iPhone12 miniを修理したい。予算3万以内でカメラユニットが動くジャンク品を探して」
    → keyword="iPhone12 mini", max_price=30000, junk_only=True, working_parts="カメラ"

    「状態の良いiPadを5万以内で」
    → keyword="iPad", max_price=50000, junk_only=False

    「画面は割れててもいい、充電だけできるiPhone11のジャンク」
    → keyword="iPhone11", junk_only=True, working_parts="充電"

    Args:
        keyword: 商品名・モデル名・ブランド（例: iPhone12 mini, SONY, ギター）
        max_price: 予算上限（円）。「3万以内」→ 30000
        min_price: 下限価格（円）
        category: スマートフォン / タブレット / 楽器 / オーディオ / PC
        brand: Apple / SONY / YAMAHA / Fender など
        junk_only: True=ジャンクのみ / False=通常中古のみ / None=両方
        working_parts: 動作確認必須パーツをカンマ区切りで（例: カメラ,バッテリー）
        broken_parts: 除外したい故障内容をカンマ区切りで（例: 画面割れ,タッチ不良）
    """
    results = INVENTORY

    if keyword:
        kw = keyword.lower()
        results = [i for i in results if
                   kw in i["name"].lower() or
                   kw in i["brand"].lower() or
                   kw in i["category"].lower() or
                   kw in i["notes"].lower()]

    if max_price is not None:
        results = [i for i in results if i["price"] <= max_price]

    if min_price is not None:
        results = [i for i in results if i["price"] >= min_price]

    if category:
        results = [i for i in results if i["category"] == category]

    if brand:
        results = [i for i in results if brand.lower() in i["brand"].lower()]

    if junk_only is True:
        results = [i for i in results if i["junk"]]
    elif junk_only is False:
        results = [i for i in results if not i["junk"]]

    if working_parts:
        required = [p.strip() for p in working_parts.split(",")]
        results = [
            i for i in results
            if i["junk"] and all(r in i["working_parts"] for r in required)
        ]

    if broken_parts:
        exclude = [p.strip() for p in broken_parts.split(",")]
        results = [
            i for i in results
            if not any(e in i["broken_parts"] for e in exclude)
        ]

    if not results:
        return "条件に合う商品は見つかりませんでした。"

    lines = [f"【検索結果: {len(results)}件】\n"]
    for item in results:
        lines.append(
            f"ID:{item['id']} {item['name']}\n"
            f"  価格: ¥{item['price']:,} / 状態: {item['condition']} / 店舗: {item['store']}\n"
            f"  {item['notes']}\n"
        )
    return "\n".join(lines)


@mcp.tool()
def get_item_detail(item_id: int) -> str:
    """
    商品IDで詳細情報を取得します。
    search_used_itemsで見つけた商品の詳細確認や、取り置き前の確認に使います。

    Args:
        item_id: 商品ID（search_used_itemsの結果に含まれるID）
    """
    item = next((i for i in INVENTORY if i["id"] == item_id), None)
    if not item:
        return f"ID:{item_id} の商品は見つかりませんでした。"

    wp = "、".join(item["working_parts"]) if item["working_parts"] else "なし（通常中古）"
    bp = "、".join(item["broken_parts"]) if item["broken_parts"] else "なし"

    return (
        f"【商品詳細】\n"
        f"ID       : {item['id']}\n"
        f"商品名   : {item['name']}\n"
        f"価格     : ¥{item['price']:,}\n"
        f"状態     : {item['condition']}\n"
        f"店舗     : {item['store']}\n"
        f"カテゴリ : {item['category']}\n"
        f"ブランド : {item['brand']}\n"
        f"動作部位 : {wp}\n"
        f"不具合   : {bp}\n"
        f"備考     : {item['notes'] or 'なし'}\n"
    )


# ── 起動 ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    import uvicorn
    from starlette.types import ASGIApp, Receive, Scope, Send

    class FixHostMiddleware:
        def __init__(self, app: ASGIApp):
            self.app = app

        async def __call__(self, scope: Scope, receive: Receive, send: Send):
            if scope["type"] in ("http", "websocket"):
                headers = [(k, v) for k, v in scope.get("headers", [])
                           if k.lower() != b"host"]
                headers.append((b"host", b"localhost"))
                scope["headers"] = headers
            await self.app(scope, receive, send)

    port = int(os.environ.get("PORT", 8000))
    app = FixHostMiddleware(mcp.sse_app())
    uvicorn.run(app, host="0.0.0.0", port=port)
