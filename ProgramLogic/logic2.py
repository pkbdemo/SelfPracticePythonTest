from collections import Counter
message = "Hello welcome to Cathay 60th year anniversary"
# 轉換小寫，計算字母出現次數
message = message.lower()
letterCounts = Counter(message)

#  每個字母出現次數
for letter, count in letterCounts.items():
    if letter.isalpha():  # 檢查是否為字母
        print(f"{letter}: {count}")