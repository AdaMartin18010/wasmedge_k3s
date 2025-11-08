#!/bin/bash
# 技术版本检查脚本
# 用途：检查技术组件的版本发布状态
# 创建日期：2025-11-07

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Kubernetes 版本
check_kubernetes() {
    local version=$1
    log_info "检查 Kubernetes $version 发布状态..."

    # 检查 GitHub Releases
    local url="https://api.github.com/repos/kubernetes/kubernetes/releases"
    local response=$(curl -s "$url" | grep -o "\"tag_name\":\"v${version}\.[0-9]*\"" | head -1)

    if [ -n "$response" ]; then
        log_info "✅ Kubernetes $version 已发布"
        echo "$response"
        return 0
    else
        # 检查是否有更高版本
        local latest=$(curl -s "$url" | grep -o "\"tag_name\":\"v[0-9]*\.[0-9]*\.[0-9]*\"" | head -1 | grep -o "v[0-9]*\.[0-9]*")
        if [ -n "$latest" ]; then
            log_warn "⚠️  Kubernetes $version 未找到，最新版本为 $latest"
        else
            log_warn "⚠️  Kubernetes $version 未找到或未发布（无法获取最新版本信息）"
        fi
        return 1
    fi
}

# 检查 K3s 版本
check_k3s() {
    local version=$1
    log_info "检查 K3s $version 发布状态..."

    # 检查 GitHub Releases
    local url="https://api.github.com/repos/k3s-io/k3s/releases"
    local response=$(curl -s "$url" | grep -o "\"tag_name\":\"v${version}\.[0-9]*+k3s[0-9]*\"" | head -1)

    if [ -n "$response" ]; then
        log_info "✅ K3s $version 已发布"
        echo "$response"
        return 0
    else
        # 检查是否有更高版本
        local latest=$(curl -s "$url" | grep -o "\"tag_name\":\"v[0-9]*\.[0-9]*\.[0-9]*+k3s[0-9]*\"" | head -1 | grep -o "v[0-9]*\.[0-9]*")
        if [ -n "$latest" ]; then
            log_warn "⚠️  K3s $version 未找到，最新版本为 $latest"
        else
            log_warn "⚠️  K3s $version 未找到或未发布（无法获取最新版本信息）"
        fi
        return 1
    fi
}

# 检查 WasmEdge 版本
check_wasmedge() {
    local version=$1
    log_info "检查 WasmEdge $version 发布状态..."

    # 检查 GitHub Releases
    local url="https://api.github.com/repos/WasmEdge/WasmEdge/releases"
    local response=$(curl -s "$url" | grep -o "\"tag_name\":\"${version}\.[0-9]*\"" | head -1)

    if [ -n "$response" ]; then
        log_info "✅ WasmEdge $version 已发布"
        echo "$response"
        return 0
    else
        log_warn "⚠️  WasmEdge $version 未找到或未发布"
        return 1
    fi
}

# 检查 Gatekeeper 版本
check_gatekeeper() {
    local version=$1
    log_info "检查 Gatekeeper $version 发布状态..."

    # 检查 GitHub Releases
    local url="https://api.github.com/repos/open-policy-agent/gatekeeper/releases"
    local response=$(curl -s "$url" | grep -o "\"tag_name\":\"v${version}\.[0-9]*\"" | head -1)

    if [ -n "$response" ]; then
        log_info "✅ Gatekeeper $version 已发布"
        echo "$response"
        return 0
    else
        log_warn "⚠️  Gatekeeper $version 未找到或未发布"
        return 1
    fi
}

# 主函数
main() {
    log_info "开始技术版本检查..."
    echo ""

    # 检查 Kubernetes
    check_kubernetes "1.30"
    echo ""

    # 检查 K3s
    check_k3s "1.30"
    echo ""

    # 检查 WasmEdge
    check_wasmedge "0.14"
    echo ""

    # 检查 Gatekeeper
    check_gatekeeper "3.15"
    echo ""

    log_info "版本检查完成"
}

# 运行主函数
main "$@"

