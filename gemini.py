# gemini_client.py

from google import genai
from dotenv import load_dotenv

load_dotenv()

# Client init faqat bir marta
client = genai.Client()

def get_price_from_gemini(parametr: str) -> int:
    """
    Berilgan parametr bo‘yicha mahsulot/xizmatning 
    Toshkentdagi o‘rtacha narxini Gemini orqali qaytaradi.
    Natija son ko‘rinishida bo‘ladi: masalan 8500000
    """
    prompt = (
        f"Quyidagi parametrli xizmat yoki maxsulotning toshkent "
        f"shahridagi o'rtacha narxi qanday: {parametr}. "
        "Natijani faqat son ko'rinishida qaytar (masalan: 8500000)."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        # faqat sonlarni ajratib olish
        text = response.text.strip()
        num = int("".join(filter(str.isdigit, text)))
        return num
    except:
        return None
def get_price_from_gemini_predict(parametr: str) -> int:

    prompt = (
        f"Quyidagi matndan maxsulot yoki xizmat ni top va unga berilgan narxni qaytar. Agar matnda maxsulot yoki xizmat va uning narxi mavjud bo'lmasa shartnoma emas deb qaytar"
        f"Matn {parametr}. "
        f"Agar mavjud bo'lsa berilgan narx xizmat uchun qimmat emasmi? Necha foizga qimmatligini keltir. O'z taxminiy xulosalaringni keltir Toshkent shahridagi narxlardan kelib chiqib. Taxminiy natijani faqat necha foiz qimmatligini keltir ortiqcha izohlarsi. Kutilgan narxni ham keltir."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        # faqat sonlarni ajratib olish
        text = response.text
        return text
    except:
        return None