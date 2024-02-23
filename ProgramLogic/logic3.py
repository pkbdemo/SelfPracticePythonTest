def FindPosition(n):
    list_ = [0] * n 
    k = n
    yo = 0  #  報數
    index = 0  # 索引

    while k != 1: #如果剩下一人結束循環
        if index >= len(list_):  
            index = 0
        if list_[index] == 0:
            yo += 1  # 增加計數器
            if yo == 3: #如果這個人報的數字是3，把其數組值設為-1，代表他退出圈子,人數k-1。然後重新從1報數
                list_[index] = -1  
                k -= 1 
                yo = 0 
        index += 1 

    
    for i in range(len(list_)):
        if list_[i] == 0:
            return i + 1 #最後留下來的是第幾位

    return -1  #如果沒有符合條件的元素，返回 -1

n = int(input("請輸入一個數字："))
result = FindPosition(n)
print(f"最後留下的是第幾位：{result}")