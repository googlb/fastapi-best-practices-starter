.PHONY: help install dev start test lint format clean init-admin

# 默认目标
help:
	@echo "可用命令:"
	@echo "  make install     - 安装项目依赖"
	@echo "  make dev         - 启动开发服务器 (端口8001)"
	@echo "  make start       - 启动服务器 (端口8000)"
	@echo "  make test        - 运行测试"
	@echo "  make lint        - 代码检查"
	@echo "  make format      - 代码格式化"
	@echo "  make clean       - 清理缓存文件"
	@echo "  make init-admin  - 初始化管理员用户 (admin/123456)"

# 安装依赖
install:
	uv sync --dev

# 开发模式启动 (端口8001)
dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 生产模式启动 (端口8000)
start:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
test:
	uv run pytest

# 代码检查
lint:
	uv run ruff check app/
	uv run mypy app/

# 代码格式化
format:
	uv run ruff format app/

# 清理缓存
clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# 初始化管理员用户
init-admin:
	uv run python scripts/init_admin.py
