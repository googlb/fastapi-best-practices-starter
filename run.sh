#!/bin/bash

# FastAPI 项目启动脚本
# 使用方法: ./run.sh [命令]

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  FastAPI 项目管理脚本${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 显示帮助信息
show_help() {
    print_header
    echo "使用方法: ./run.sh [命令]"
    echo ""
    echo "可用命令:"
    echo "  install     安装项目依赖"
    echo "  dev         启动开发服务器 (端口8001)"
    echo "  start       启动服务器 (端口8000)"
    echo "  test        运行测试"
    echo "  lint        代码检查"
    echo "  format      代码格式化"
    echo "  clean       清理缓存文件"
    echo "  init-admin  初始化管理员用户 (admin/123456)"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  ./run.sh dev     # 启动开发服务器"
    echo "  ./run.sh test    # 运行测试"
    echo "  ./run.sh init-admin  # 初始化管理员用户"
}

# 检查是否安装了uv
check_uv() {
    if ! command -v uv &> /dev/null; then
        print_error "未找到 uv 命令，请先安装 uv: https://docs.astral.sh/uv/"
        exit 1
    fi
}

# 安装依赖
install_deps() {
    print_message "正在安装项目依赖..."
    uv sync --dev
    if [ $? -eq 0 ]; then
        print_message "依赖安装成功!"
    else
        print_error "依赖安装失败!"
        exit 1
    fi
}

# 启动开发服务器
start_dev() {
    print_message "正在启动开发服务器 (端口8001)..."
    print_message "访问 http://localhost:8001 查看应用"
    print_message "访问 http://localhost:8001/docs 查看API文档"
    print_warning "按 Ctrl+C 停止服务器"
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
}

# 启动生产服务器
start_prod() {
    print_message "正在启动服务器 (端口8000)..."
    print_message "访问 http://localhost:8000 查看应用"
    print_message "访问 http://localhost:8000/docs 查看API文档"
    print_warning "按 Ctrl+C 停止服务器"
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# 运行测试
run_tests() {
    print_message "正在运行测试..."
    uv run pytest
}

# 代码检查
run_lint() {
    print_message "正在进行代码检查..."
    uv run ruff check app/
    uv run mypy app/
}

# 代码格式化
run_format() {
    print_message "正在进行代码格式化..."
    uv run ruff format app/
}

# 清理缓存
clean_cache() {
    print_message "正在清理缓存文件..."
    find . -type d -name "__pycache__" -delete
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    rm -rf .coverage
    rm -rf htmlcov/
    rm -rf .pytest_cache/
    rm -rf .mypy_cache/
    print_message "缓存清理完成!"
}

# 初始化管理员用户
init_admin() {
    print_message "正在初始化管理员用户..."
    uv run python scripts/init_admin.py
}

# 主函数
main() {
    # 检查是否安装了uv
    check_uv

    # 根据参数执行不同命令
    case "${1:-help}" in
        "install")
            install_deps
            ;;
        "dev")
            start_dev
            ;;
        "start")
            start_prod
            ;;
        "test")
            run_tests
            ;;
        "lint")
            run_lint
            ;;
        "format")
            run_format
            ;;
        "clean")
            clean_cache
            ;;
        "init-admin")
            init_admin
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# 执行主函数
main "$@"
