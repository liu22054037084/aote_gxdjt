#!/bin/bash

CHCP 65001

for /f "tokens=2 delims==" %%a in ('wmic path win32_operatingsystem get LocalDateTime /value') do (set t=%%a)

set Today="%t:~0,4%年%t:~4,2%月%t:~6,2%日%t:~8,2%时%t:~10,2%分%t:~12,2%秒"

git add .

git pull origin main

git commit -m %Today%

git push -u origin main

EXIT  