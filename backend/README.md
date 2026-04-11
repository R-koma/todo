# Todo Agent App — Backend

FastAPI + PostgreSQL で構築した、タスク管理のための CRUD REST API バックエンドです。

## 技術スタック

- **FastAPI** (Python 3.13+) — Web フレームワーク
- **asyncpg** — 非同期 PostgreSQL ドライバ（クエリに直接使用）
- **Alembic** — データベースマイグレーション（SQLAlchemy はマイグレーションのみ使用）
- **Pydantic v2** — リクエスト / レスポンスのバリデーション
- **PostgreSQL 17** — データベース（Docker で起動）
- **uv** — Python パッケージマネージャー

## プロジェクト構成

```
backend/
├── main.py                    # FastAPI エントリーポイント
├── config.py                  # 環境変数読み込み
├── database.py                # asyncpg 接続プール・依存性注入
├── routes/
│   └── task.py                # ルートハンドラー
├── schemas/
│   └── task.py                # Pydantic モデル
├── repositories/
│   └── task_repository.py     # SQL クエリレイヤー
└── migrations/                # Alembic マイグレーション
    └── versions/
        └── 999bb0d567ed_create_tasks_table.py
```

## データベーススキーマ

**テーブル名:** `tasks`

| カラム       | 型          | 制約                                                                              |
| ------------ | ----------- | --------------------------------------------------------------------------------- |
| `id`         | UUID        | PRIMARY KEY, `gen_random_uuid()`                                                  |
| `title`      | TEXT        | NOT NULL                                                                          |
| `status`     | TEXT        | NOT NULL, DEFAULT `'in_progress'`, CHECK: `'in_progress'` または `'is_completed'` |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT `NOW()`                                                         |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT `NOW()`                                                         |

## 事前準備

以下のツールをインストールしてください。

- [Docker](https://www.docker.com/)
- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## セットアップ手順

**1. `.env` ファイルを作成する**

プロジェクトルート（`docker-compose.yml` と同じ階層）に `.env` を作成します。

```env
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev
POSTGRES_DB=todo_agent
DATABASE_URL=postgresql://dev:dev@localhost:5433/todo_agent
```

**2. PostgreSQL を起動する**

```bash
docker-compose up -d
```

PostgreSQL 17 がポート `5433` で起動します。

**3. 依存パッケージをインストールする**

```bash
cd backend
uv sync
```

**4. マイグレーションを実行する**

```bash
uv run alembic upgrade head
```

**5. 開発サーバーを起動する**

```bash
uv run fastapi dev main.py
```

サーバーが `http://localhost:8000` で起動します。

## API リファレンス

| メソッド | エンドポイント         | 説明           | リクエストボディ                            | レスポンス         |
| -------- | ---------------------- | -------------- | ------------------------------------------- | ------------------ |
| `GET`    | `/api/tasks`           | タスク一覧取得 | —                                           | `{"tasks": [...]}` |
| `POST`   | `/api/tasks`           | タスク作成     | `{"title": "string"}`                       | `TaskResponse`     |
| `PATCH`  | `/api/tasks/{task_id}` | タスク更新     | `{"title"?: "string", "status"?: "string"}` | `TaskResponse`     |
| `DELETE` | `/api/tasks/{task_id}` | タスク削除     | —                                           | `204 No Content`   |

> 新規作成されたタスクの `status` は常に `"in_progress"` になります。

**TaskResponse**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "買い物をする",
  "status": "in_progress",
  "created_at": "2026-04-11T10:00:00+00:00",
  "updated_at": "2026-04-11T10:00:00+00:00"
}
```

**エラーレスポンス**

存在しない `task_id` を指定した場合、`404 Not Found` が返ります。

```json
{ "detail": "Task not found" }
```

## API ドキュメント

FastAPI の自動生成ドキュメントをブラウザで確認できます（サーバー起動後）。

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
