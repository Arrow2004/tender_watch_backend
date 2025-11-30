from pdf import extract_value, clean_text_number

file_path = "uploads/Договор_№3899803_национальный_магазин.pdf"

count = extract_value(file_path, "Сони", "column")
parametr = extract_value(file_path, "Техник параметрлар", "row")
bitim_summasi = extract_value(file_path, "Битим\nсуммаси", "column")

print("Soni:", clean_text_number(count.get("value")))
print("Texnik parametrlar:", parametr.get("value"))
print("Bitim summasi:", clean_text_number(bitim_summasi.get("value")) / 1000, "ming UZS")