point1 = (3,5)
point2 = (7, 2)
print(f"point1: {point1}")
print(f"point2: {point2}")

x1, y1 = point1
x2, y2 = point2 
print(f"X1={x1}, Y1={y1}")
print(f"X2={x2}, Y2={y2}") 

distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
print(f"Distance between point1 and point2: {distance}")