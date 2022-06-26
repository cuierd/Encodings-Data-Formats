
# sample solution
with open("encoding_1.txt", "r", encoding="ASCII") as e1:
    with open("encoding_2.txt", "r", encoding="ISO_8859-1") as e2:
        with open("encoding_utf-8.txt", "w", encoding="utf-8") as f:
            e1_text = e1.read()
            e2_text = e2.read()
            f.write(e1_text)
            f.write(e2_text)



