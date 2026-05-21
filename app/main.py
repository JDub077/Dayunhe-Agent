import os
from contextlib import asynccontextmanager

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base, SessionLocal
from app.routers import characters, sessions, chat
from app.models.character import Character


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 创建表 + 初始化角色数据
    Base.metadata.create_all(bind=engine)
    init_characters()
    yield
    # Shutdown


def init_characters():
    db = SessionLocal()
    try:
        existing = db.query(Character).count()
        if existing > 0:
            return

        # 从 YAML 读取林文绮
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "lin-wenqi.yaml")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        else:
            data = {}

        characters_data = [
            {
                "id": data.get("id", "lin-wenqi"),
                "name": data.get("name", "林文绮"),
                "title": data.get("title", "漕兵"),
                "era": data.get("era", "永乐十九年"),
                "avatar_url": data.get("avatar_url", ""),
                "tagline": data.get("tagline", "容貌秀丽，面有易容痕迹"),
                "tags": data.get("tags", ["果敢", "隐忍", "军中女子"]),
                "system_prompt": data.get("system_prompt", ""),
                "few_shots": data.get("few_shots", []),
                "knowledge_nodes": data.get("knowledge_nodes", []),
                "secrets": data.get("secrets", []),
            },
            # 其他4个角色占位（后续 Prompt 完善后替换 system_prompt）
            {
                "id": "wang-huaiyuan",
                "name": "王淮远",
                "title": "官员",
                "era": "永乐十九年",
                "tagline": "忠直官员，关切皇粮",
                "tags": ["忠直", "凝重", "问责"],
                "system_prompt": "你是王淮远，永乐十九年官员。年近而立，身量中等偏上，眉目清朗，蓄短须。你关切皇粮，对赵秉丰有怀疑。",
                "few_shots": [],
            },
            {
                "id": "zheng-chaosheng",
                "name": "郑潮生",
                "title": "苦力",
                "era": "永乐十九年",
                "tagline": "眉骨有月牙疤，神色恍惚",
                "tags": ["底层", "恍惚", "隐忍"],
                "system_prompt": "你是郑潮生，永乐十九年苦力。二十上下，披着布棉袄，眉骨上有块浅浅的月牙形疤痕，神色恍惚。你有不可告人的秘密。",
                "few_shots": [],
            },
            {
                "id": "zhao-bingfeng",
                "name": "赵秉丰",
                "title": "商人",
                "era": "永乐十九年",
                "tagline": "体态微宽，面容和善却憔悴",
                "tags": ["奸商", "和善", "憔悴"],
                "system_prompt": "你是赵秉丰，永乐十九年商人。已过不惑，体态微宽，面容和善却憔悴。你家的船出了问题。",
                "few_shots": [],
            },
            {
                "id": "su-xiuyun",
                "name": "苏岫云",
                "title": "民女",
                "era": "永乐十九年",
                "tagline": "体态纤弱，愁颜不展",
                "tags": ["病弱", "复仇者", "隐忍"],
                "system_prompt": "你是苏岫云，永乐十九年民女。十八九岁，身着青色衣裙，体态纤弱，愁颜不展，时不时低低咳嗽。你身上有玉佩，背负着复仇的使命。",
                "few_shots": [],
            },
        ]

        for c in characters_data:
            db.add(Character(**c))
        db.commit()
    finally:
        db.close()


app = FastAPI(
    title="明舟北渡 · 角色智能体 API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
