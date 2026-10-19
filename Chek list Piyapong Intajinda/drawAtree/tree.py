def draw_tree(height):
    # วาดส่วนใบของต้นไม้ (ทรงสามเหลี่ยม)
    for i in range(height):
        spaces = " " * (height - i - 1)
        hashes = "#" * (2 * i + 1)
        print(spaces + hashes)
    
    # วาดส่วนลำต้น
    trunk_spaces = " " * (height - 1)
    for _ in range(2):  # กำหนดความยาวของลำต้นเป็น 2 บรรทัด
        print(trunk_spaces + "#")

# เรียกใช้งานฟังก์ชัน (สามารถกำหนดความสูงของต้นไม้ได้ในวงเล็บ)
draw_tree(5)