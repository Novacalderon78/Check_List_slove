import math

def dot_product(v1, v2):
    """คำนวณหา Dot Product ของเวกเตอร์ 2 ตัว"""
    return sum(a * b for a, b in zip(v1, v2))

def vector_length(v):
    """คำนวณหาความยาว (Magnitude) ของเวกเตอร์"""
    return math.sqrt(sum(a ** 2 for a in v))

# ตัวอย่างเวกเตอร์ 2 มิติ หรือ 3 มิติ
u = [3, 4, 0]
v = [1, 2, 2]

# คำนวณผลลัพธ์
dot_result = dot_product(u, v)
length_u = vector_length(u)
length_v = vector_length(v)

print(f"Dot Product (u · v): {dot_result}")
print(f"ความยาวเวกเตอร์ u (|u|): {length_u}")
print(f"ความยาวเวกเตอร์ v (|v|): {length_v}")