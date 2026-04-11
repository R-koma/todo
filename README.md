# Todo Agent App

タスク管理のための Web アプリケーションです。FastAPI バックエンドと PostgreSQL データベースで構成されています。

## 技術スタック

| レイヤー       | 技術                              |
| -------------- | --------------------------------- |
| バックエンド   | FastAPI (Python 3.13+), asyncpg   |
| データベース   | PostgreSQL 17                     |
| インフラ       | Docker, docker-compose            |
| パッケージ管理 | uv                                |

## プロジェクト構成

```
todo-agent-app/
├── docker-compose.yml     # PostgreSQL コンテナ定義
├── backend/               # FastAPI アプリケーション
│   └── README.md          # バックエンド詳細ドキュメント
└── frontend/              # フロントエンド（準備中）
```

## クイックスタート

### 1. `.env` ファイルを作成する

プロジェクトルートに `.env` を作成します。

```env
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev
POSTGRES_DB=todo_agent
DATABASE_URL=postgresql://dev:dev@localhost:5433/todo_agent
```

### 2. PostgreSQL を起動する

```bash
docker-compose up -d
```

PostgreSQL 17 がポート `5433` で起動します。

### 3. バックエンドをセットアップして起動する

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run fastapi dev main.py
```

サーバーが `http://localhost:8000` で起動します。

## ドキュメント

- [バックエンド詳細](./backend/README.md) — API リファレンス、DB スキーマ、詳細セットアップ手順
- **Swagger UI:** http://localhost:8000/docs（サーバー起動後）
