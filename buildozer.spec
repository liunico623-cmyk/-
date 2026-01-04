[app]

# 应用基本信息
title = CountApp
package.name = countapp
package.domain = org.test

# 源码路径（相对仓库根目录）
source.dir = .
source.main = main.py

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc

# 应用版本
version = 1.0.0

# 依赖
requirements = python3,kivy

# 屏幕方向 & 全屏
orientation = portrait
fullscreen = 0

# 安卓 API 配置
android.api = 33
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a

# 锁定 build-tools 版本（防止 Buildozer 自动拉 36.x）
android.build_tools_version = 33.0.2

# 允许备份
android.allow_backup = True


[buildozer]

# 日志等级
log_level = 2
warn_on_root = 1
