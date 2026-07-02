#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# 缺依賴時先擋下，避免半途才報錯
if [ ! -d "$BACKEND_DIR/.venv" ]; then
  echo "後端虛擬環境不存在，請先執行：" >&2
  echo "  cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

if [ ! -f "$BACKEND_DIR/.env" ]; then
  echo "backend/.env 不存在，請先執行：cp backend/.env.example backend/.env 並填入設定" >&2
  exit 1
fi

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
  echo "前端依賴未安裝，請先執行：cd frontend && npm install" >&2
  exit 1
fi

if [ ! -f "$FRONTEND_DIR/.env" ]; then
  echo "frontend/.env 不存在，請先執行：cp frontend/.env.example frontend/.env" >&2
  exit 1
fi

# Ctrl+C 時兩個服務要一起收掉
cleanup() {
  echo ""
  echo "正在關閉服務..."
  kill 0 2>/dev/null || true
  exit 0
}
trap cleanup INT TERM

(
  cd "$BACKEND_DIR"
  source .venv/bin/activate
  exec uvicorn app.main:app --reload --port 8000
) &

(
  cd "$FRONTEND_DIR"
  exec npm run dev
) &

echo "後端：http://127.0.0.1:8000/docs"
echo "前端：http://localhost:5173"
echo "按 Ctrl+C 結束兩個服務"

wait
