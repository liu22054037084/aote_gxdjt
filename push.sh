#!/bin/bash

t=$(date +"%Y年%m月%d日%H时%M分%S秒")
Today="${t}"

git add .

git pull origin main

git commit -m "$Today"

git push -u origin main

exit