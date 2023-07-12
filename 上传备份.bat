#!/bin/bash

CHCP 65001

for /f "tokens=2 delims==" %%a in ('wmic path win32_operatingsystem get LocalDateTime /value') do (set t=%%a)

set Today="%t:~0,4%年%t:~4,2%月%t:~6,2%日%t:~8,2%时%t:~10,2%分%t:~12,2%秒"

git add .

git commit -m %Today%

REM 设置代理环境变量
set HTTP_PROXY=http://127.0.0.1:8889

REM 使用 git push 命令，并设置超时时间
git push -u origin main --timeout=60

REM 检查返回值并使用本地代理代理
IF %ERRORLEVEL% NEQ 0 (
  git config --global http.proxy %HTTP_PROXY%
  git push -u origin main
  git config --global --unset HTTP_PROXY
)

EXIT
