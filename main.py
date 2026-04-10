"""
中古ショップ AI API
- APIはシンプルな検索エンジン
- 自然言語の解釈はClaudeアプリ側が行う
- MCPのツール説明文を丁寧に書くことでClaudeが賢く使いこなせる
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="中古ショップ AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 在庫データ ─────────────────────────────────────────────────────
# junk=True の商品は working_parts / broken_parts を記載
INVENTORY = [
    # ─ スマートフォン（通常中古）
    {"id": 1,  "name": "Apple iPhone 13 128GB ミッドナイト",          "price": 52000, "store": "ハードオフ 新宿店",   "condition": "中古A",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "スマートフォン", "brand": "Apple",    "notes": "SIMフリー・バッテリー91%"},
    {"id": 2,  "name": "Apple iPhone 12 mini 64GB ブラック",           "price": 24800, "store": "ハードオフ 渋谷店",   "condition": "中古B",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "スマートフォン", "brand": "Apple",    "notes": "SIMフリー・バッテリー85%"},
    {"id": 3,  "name": "Apple iPhone SE 第3世代 64GB スターライト",    "price": 29800, "store": "ゲオ 渋谷店",         "condition": "中古A",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "スマートフォン", "brand": "Apple",    "notes": "SIMフリー・付属品完備"},
    # ─ スマートフォン（ジャンク）
    {"id": 4,  "name": "Apple iPhone 12 mini 64GB ホワイト",           "price": 8800,  "store": "ハードオフ 渋谷店",   "condition": "ジャンク",  "junk": True,  "working_parts": ["カメラ", "バッテリー", "スピーカー"], "broken_parts": ["画面割れ", "タッチ不良"],   "category": "スマートフォン", "brand": "Apple",    "notes": "画面割れ・タッチ不良。カメラ・バッテリー・スピーカー動作確認済み"},
    {"id": 5,  "name": "Apple iPhone 12 mini 128GB ブラック",          "price": 12000, "store": "ハードオフ 吉祥寺店", "condition": "ジャンク",  "junk": True,  "working_parts": ["カメラ", "画面", "タッチ", "充電"],   "broken_parts": ["充電不良"],                 "category": "スマートフォン", "brand": "Apple",    "notes": "充電コネクタ不良。画面・タッチ・カメラは正常動作"},
    {"id": 6,  "name": "Apple iPhone 12 64GB レッド",                  "price": 7500,  "store": "オフハウス 池袋店",   "condition": "ジャンク",  "junk": True,  "working_parts": ["カメラ", "タッチ", "充電"],           "broken_parts": ["液晶不良（バックライト弱）"], "category": "スマートフォン", "brand": "Apple",    "notes": "バックライト弱め。カメラ・タッチ・充電は正常"},
    {"id": 7,  "name": "Apple iPhone 11 128GB ブラック",               "price": 6800,  "store": "ハードオフ 新宿店",   "condition": "ジャンク",  "junk": True,  "working_parts": ["画面", "タッチ", "充電", "スピーカー"], "broken_parts": ["カメラ不良（AF不可）"],    "category": "スマートフォン", "brand": "Apple",    "notes": "カメラのオートフォーカス不良。画面・タッチ・充電は正常"},
    {"id": 8,  "name": "SONY Xperia 5 IV",                             "price": 11000, "store": "ハードオフ 渋谷店",   "condition": "ジャンク",  "junk": True,  "working_parts": ["カメラ", "画面", "充電"],             "broken_parts": ["SIM認識不良"],              "category": "スマートフォン", "brand": "SONY",     "notes": "SIMスロット認識不良。カメラ・画面・充電は正常"},
    # ─ タブレット
    {"id": 9,  "name": "Apple iPad Air 第4世代 64GB Wi-Fi",            "price": 28800, "store": "ハードオフ 渋谷店",   "condition": "中古B",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "タブレット",     "brand": "Apple",    "notes": ""},
    {"id": 10, "name": "Apple iPad Pro 11インチ 第2世代 128GB",         "price": 38000, "store": "ハードオフ 新宿店",   "condition": "中古A",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "タブレット",     "brand": "Apple",    "notes": ""},
    # ─ 楽器
    {"id": 11, "name": "YAMAHA アコースティックギター FG820",           "price": 24000, "store": "ハードオフ 渋谷店",   "condition": "中古B",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "楽器",           "brand": "YAMAHA",   "notes": ""},
    {"id": 12, "name": "Fender Stratocaster エレキギター（メキシコ）",  "price": 55000, "store": "ハードオフ 吉祥寺店", "condition": "中古A",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "楽器",           "brand": "Fender",   "notes": ""},
    # ─ オーディオ
    {"id": 13, "name": "SONY WH-1000XM4 ヘッドフォン",                 "price": 18500, "store": "ハードオフ 新宿店",   "condition": "中古A",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "オーディオ",     "brand": "SONY",     "notes": ""},
    {"id": 14, "name": "Marantz プリメインアンプ PM6006",               "price": 32000, "store": "ハードオフ 吉祥寺店", "condition": "中古B",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "オーディオ",     "brand": "Marantz",  "notes": ""},
    {"id": 15, "name": "Technics SL-1200MK6 ターンテーブル",            "price": 88000, "store": "ハードオフ 渋谷店",   "condition": "中古A",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "オーディオ",     "brand": "Technics", "notes": ""},
    # ─ PC
    {"id": 16, "name": "Apple MacBook Air M1 8GB 256GB",               "price": 72000, "store": "ハードオフ 新宿店",   "condition": "中古A",    "junk": False, "working_parts": [],                                    "broken_parts": [],                          "category": "PC",             "brand": "Apple",    "notes": ""},
]


# ── REST エンドポイント ────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "中古ショップ AI API 稼働中", "version": "2.0.0", "docs": "/docs"}


@app.get("/items/search")
def search_items(
    keyword:       Optional[str]  = Query(None, description="商品名・ブランド・モデル名"),
    max_price:     Optional[int]  = Query(None, description="上限価格（円）"),
    min_price:     Optional[int]  = Query(None, description="下限価格（円）"),
    category:      Optional[str]  = Query(None, description="スマートフォン / タブレット / 楽器 / オーディオ / PC"),
    brand:         Optional[str]  = Query(None, description="ブランド名"),
    junk_only:     Optional[bool] = Query(None, description="True=ジャンクのみ / False=通常中古のみ / 省略=両方"),
    working_parts: Optional[str]  = Query(None, description="動作必須パーツ（カンマ区切り）例: カメラ,バッテリー"),
    broken_parts:  Optional[str]  = Query(None, description="除外したい故障内容（カンマ区切り）例: 画面割れ,タッチ不良"),
):
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

    return {"count": len(results), "items": results}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = next((i for i in INVENTORY if i["id"] == item_id), None)
    return item if item else {"error": "商品が見つかりません"}


@app.get("/categories")
def get_categories():
    return {"categories": list(set(i["category"] for i in INVENTORY))}


# ── MCP (Model Context Protocol) ──────────────────────────────────

@app.get("/mcp/tools")
def mcp_tools():
    """
    Claudeアプリがこのエンドポイントを読み、
    ユーザーの自然言語をパラメータに変換してAPIを呼ぶ。
    説明文の充実度 = Claudeの賢さ。
    """
    return {
        "tools": [
            {
                "name": "search_used_items",
                "description": (
                    "中古ショップの在庫を検索します。\n"
                    "ユーザーの自然な発話を解釈し、適切なパラメータに変換して呼んでください。\n\n"
                    "【変換例】\n"
                    "「iPhone12 miniを修理したい。予算3万以内でカメラユニットが動くジャンク品を探して」\n"
                    "→ keyword='iPhone12 mini', max_price=30000, junk_only=True, working_parts='カメラ'\n\n"
                    "「状態の良いiPadが欲しい、5万以内で」\n"
                    "→ keyword='iPad', max_price=50000, junk_only=False\n\n"
                    "「画面は割れててもいい、充電だけできるiPhone11のジャンク」\n"
                    "→ keyword='iPhone11', junk_only=True, working_parts='充電'\n\n"
                    "「タッチが効かない以外は壊れてないジャンクiPhone」\n"
                    "→ junk_only=True, broken_parts='タッチ不良' を除外\n\n"
                    "working_parts: ジャンク品の中で「動いている必要があるパーツ」を指定\n"
                    "broken_parts:  含まれていてほしくない故障内容を指定（除外フィルター）"
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "keyword":       {"type": "string",  "description": "商品名・モデル名・ブランド（例: iPhone12 mini）"},
                        "max_price":     {"type": "integer", "description": "予算上限（円）。『3万以内』→ 30000"},
                        "min_price":     {"type": "integer", "description": "下限価格（円）"},
                        "category":      {"type": "string",  "description": "スマートフォン / タブレット / 楽器 / オーディオ / PC"},
                        "brand":         {"type": "string",  "description": "Apple / SONY / YAMAHA / Fender など"},
                        "junk_only":     {"type": "boolean", "description": "True=ジャンクのみ / False=通常中古のみ / 省略=両方"},
                        "working_parts": {"type": "string",  "description": "動作確認必須パーツをカンマ区切りで（例: カメラ,バッテリー）"},
                        "broken_parts":  {"type": "string",  "description": "除外したい故障内容をカンマ区切りで（例: 画面割れ,タッチ不良）"},
                    },
                },
            },
            {
                "name": "get_item_detail",
                "description": "商品IDで詳細を取得。search_used_itemsで見つけた商品の詳細確認に使います。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "integer", "description": "商品ID"},
                    },
                    "required": ["item_id"],
                },
            },
        ]
    }


class MCPCallRequest(BaseModel):
    tool: str
    input: dict


@app.post("/mcp/call")
def mcp_call(req: MCPCallRequest):
    if req.tool == "search_used_items":
        result = search_items(
            keyword=req.input.get("keyword"),
            max_price=req.input.get("max_price"),
            min_price=req.input.get("min_price"),
            category=req.input.get("category"),
            brand=req.input.get("brand"),
            junk_only=req.input.get("junk_only"),
            working_parts=req.input.get("working_parts"),
            broken_parts=req.input.get("broken_parts"),
        )
        return {"result": result}

    elif req.tool == "get_item_detail":
        return {"result": get_item(req.input["item_id"])}

    return {"error": f"Unknown tool: {req.tool}"}
