def swap_digits(grades):
    #  使用列表推導式交換每個數字的十位數和個位數
    swapped_grades = [int(str(grade)[::-1]) for grade in grades]
    return swapped_grades

grades = [53, 64, 75, 19, 92]
swapped_grades = swap_digits(grades)
print("原始數字列表:", grades)
print("交換後的數字列表:", swapped_grades)
