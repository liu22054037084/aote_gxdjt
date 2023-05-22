# result = []

result_list = [
    ["[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][15][GB][1080P][MP4].mp4", "2014/4/[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][15][GB][1080P][MP4].mp4"],
    ["[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][13][GB][1080P][MP4].mp4", "2014/4/[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][13][GB][1080P][MP4].mp4"],
    ["[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][12][GB][1080P][MP4].mp4", "2014/4/[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][12][GB][1080P][MP4].mp4"],
    ["[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][11][GB][1080P][MP4].mp4", "2014/4/[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][11][GB][1080P][MP4].mp4"],
    ["[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][05][GB][1080P][MP4].mp4", "2014/4/[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY][05][GB][1080P][MP4].mp4"],
    ["[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY PROLOGUE][03][GB][1080P][MP4].mp4", "2014/4/[Shirokoi][Mobile Suit Gundam THE WITCH FROM MERCURY PROLOGUE][03][GB][1080P][MP4].mp4"]
    ]

for row in result:
    result_list.append(list(row))

# 按第一列数据进行排序
sorted_result = sorted(result_list, key=lambda x: x[0])
for i in sorted_result:
    print(i[0])
