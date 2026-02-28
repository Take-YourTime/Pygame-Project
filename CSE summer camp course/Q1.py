print("輸入你的名字：", end = "")
name = input()
print("輸入你的生日：", end = "")
birthday = input()
print("輸入你朋友的名字：", end = "")
f_name = input()
print("輸入你朋友的生日：", end = "")
f_birthday = input()

print("\n我的名字是", name, "，生日是", birthday, sep = "")
print("他的名字是", f_name, "，生日是", f_birthday, "\n", sep = "")

print("今天的日期是2024/7/9，星期二")


result = float((2024 + 7 ** 9 ) / (9 - 7 + 2))
print("今天的日期的運算結果是:", result, sep = "")
a = float(((7 + 9) ** 3 - 2024) ** 0.5)
b = float((2024 // 2 + 9 * 32) ** 0.25)
print("a = ", a, ",b = ", b, sep = "")
print("Q:A大於B嗎？")
print(a > b)

