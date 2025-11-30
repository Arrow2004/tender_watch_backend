from fastapi import FastAPI, File, UploadFile
import shutil
import os
from pdf import extract_value, clean_text_number, get_text_from_pdf
from gemini import get_price_from_gemini,get_price_from_gemini_predict

app = FastAPI()

UPLOAD_DIR = "uploads"

# uploads papkasini avtomatik yaratish
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Faqat PDF formatini tekshirish
    if file.content_type != "application/pdf":
        return {"error": "Faqat PDF yuklash mumkin!"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)
        # Faylni saqlash
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        # PDF dan ma'lumotlarni chiqarish
        count = extract_value(file_path, "Сони", "column")
        parametr = extract_value(file_path, "Техник параметрлар", "row")
        bitim_summasi = extract_value(file_path, "Битим\nсуммаси", "column")
        narx = get_price_from_gemini(parametr["value"])
        os.remove(file_path)
        return {"message": "PDF muvaffaqiyatli yuklandi", "file_path": file_path, "count": count.get('value'), "parametr": parametr.get("value"), "bitim_summasi": clean_text_number(bitim_summasi.get("value")) / 100, "Kutilgan summa": narx}

    except Exception as e:
        result = get_text_from_pdf(file_path)
        if result["result"] == False:
            os.remove(file_path)
            return {"error": result["Matn"]}
        gemini_result = get_price_from_gemini_predict(result["Matn"])
        os.remove(file_path)
        return {"error": f"PDF dan ma'lumotlarni chiqarishda xatolik yuz berdi: {str(e)}", "olingan matn": result.get("Matn"), "gemini natija": gemini_result}
   