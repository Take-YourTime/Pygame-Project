import math

def circle_location(r, angle): 
    # r: 圓半徑
    # angle: 0 degree ~ 360 degree
    angle = math.radians(angle) # 度數轉弧度
    return r * math.sin(angle), -r * math.cos(angle)

