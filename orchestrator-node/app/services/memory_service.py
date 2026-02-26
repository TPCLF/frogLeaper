from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Optional

import aiosqlite

from app.schemas import Message
from app.services.embedding_service import HashEmbeddingService


@dataclass
class MemoryItem:
    role: str
    content: str
    score: float


class MemoryService:
    def __init__(self, db_path: str, embedding_dim: int = 384) -> None:
        self.db_path = db_path
        self.embedding = HashEmbeddingService(dim=embedding_dim)

    async def init(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS summaries (
                    conversation_id TEXT PRIMARY KEY,
                    summary_text TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            await db.commit()

    async def add_message(self, conversation_id: str, message: Message) -> None:
        emb = self.embedding.embed_text(message.content)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO messages (conversation_id, role, content, embedding)
                VALUES (?, ?, ?, ?)
                """,
                (conversation_id, message.role, message.content, json.dumps(emb)),
            )
            await db.commit()

    async def get_recent_messages(self, conversation_id: str, limit: int) -> List[Message]:
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                """
                SELECT role, content FROM messages
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (conversation_id, limit),
            )
            rows = await cur.fetchall()
        rows.reverse()
        return [Message(role=row[0], content=row[1]) for row in rows]

    async def get_message_count(self, conversation_id: str) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "SELECT COUNT(*) FROM messages WHERE conversation_id = ?",
                (conversation_id,),
            )
            row = await cur.fetchone()
        return int(row[0])

    async def get_semantic_memories(self, conversation_id: str, query: str, top_k: int = 5) -> List[MemoryItem]:
        query_emb = self.embedding.embed_text(query)
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                """
                SELECT role, content, embedding FROM messages
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT 300
                """,
                (conversation_id,),
            )
            rows = await cur.fetchall()

        scored: List[MemoryItem] = []
        for role, content, emb_json in rows:
            emb = json.loads(emb_json)
            score = self.embedding.cosine_similarity(query_emb, emb)
            scored.append(MemoryItem(role=role, content=content, score=score))

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]

    async def upsert_summary(self, conversation_id: str, summary_text: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO summaries (conversation_id, summary_text, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(conversation_id)
                DO UPDATE SET summary_text = excluded.summary_text, updated_at = CURRENT_TIMESTAMP
                """,
                (conversation_id, summary_text),
            )
            await db.commit()

    async def get_summary(self, conversation_id: str) -> Optional[str]:
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "SELECT summary_text FROM summaries WHERE conversation_id = ?",
                (conversation_id,),
            )
            row = await cur.fetchone()
        return row[0] if row else None
