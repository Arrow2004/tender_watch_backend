import pdfplumber
import re


def extract_value(file: str, search_value: str, search_type: str):
    """
    search_type:
        - "column" → ustun nomi bo‘yicha qiymat olish
        - "row" → qator nomi bo‘yicha qiymat olish
    """

    with pdfplumber.open(file) as pdf:
        for page_index, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if not tables:
                continue

            for table_index, table in enumerate(tables):

                # -----------------------
                # 1) COLUMN SEARCH
                # -----------------------
                if search_type == "column":
                    headers = table[0]
                    if not headers:
                        continue

                    try:
                        col_index = headers.index(search_value)
                    except ValueError:
                        continue

                    if len(table) > 1 and len(table[1]) > col_index:
                        return {
                            "type": "column",
                            "column_name": search_value,
                            "value": table[1][col_index],
                            "table_index": table_index,
                            "page_index": page_index
                        }

                # -----------------------
                # 2) ROW SEARCH
                # -----------------------
                elif search_type == "row":
                    for row in table:
                        if row and row[0] and search_value in str(row[0]):
                            return {
                                "type": "row",
                                "row_name": search_value,
                                "value": row[1] if len(row) > 1 else None,
                                "table_index": table_index,
                                "page_index": page_index
                            }

    return None

def get_text_from_pdf(file: str) -> str:
    result = {"result": True, "Matn": ""}
    with pdfplumber.open(file) as pdf:
        if len(pdf.pages) == 0:
            result =  {"result": False, "Matn": "PDF faylida sahifalar mavjud emas."}
        elif len(pdf.pages) > 5:
            result = {"result": False, "Matn": "PDF faylida juda ko'p sahifalar mavjud."}
        else:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            result["Matn"] = full_text
    return result

def clean_text_number(text: str) -> int:
    if not text:
        return 0
    text = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()
    return int(re.sub(r'[^\d]', '', text))
