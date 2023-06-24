import re

filename = "[orion origin] Tengoku Daimakyou [01] [1080p] [H265 AAC] [CHS＆JPN].mp4"
modified_filename = re.sub(r'(?:\[|\(|\{|\s)(\d+)(?:\s*v\s*\d+)?(?:]|\)|}|\s)(\[\d*v\d]|\(\d*v\d\)|\[V\d]|\(V\d\))?.*', "", filename)

print(f"'{modified_filename}'")
