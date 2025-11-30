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
        f"Agar mavjud bo'lsa berilgan narx xizmat uchun qimmat emasmi? Necha foizga qimmatligini keltir. O'z taxminiy xulosalaringni Toshkent shahridagi narxlardan kelib chiqqan xolda hisobla va taxminiy natijani quyidagicha qaytar(Ortiqcha stylelar kerak emas bold, italic yoki xar xil emojilar):"
        f"Xizmat turi: [Sen aniqlagan xizmat nomi]"
        f"Bitim narxi: [Shartnomada keltirilgan narx]"
        f"Taxminiy Toshkent narxi: [Toshkent shahridagi o'rtacha narx]"
        f"Qimmatlik darajasi: [Necha foizga qimmat yoki arzonligini keltir]"
        f"Xulosa: [Shubhali bo'lmagan narx/ Juda qimmat / Shubxali darajada qimmat]"
        f"Agar 25-30% ga qimmatlik qilsa juda qimmat deb hisoblama, ammo 60% da yuqori bo'lsa juda qimmat va 100% dan baland bo'lsa shubxali qimmat deb keltir"
        f"Agar bu qandaydur shartnoma emas deb o'ylasang: Berilgan file shartnomaga o'xshamayapti. Iltimos namunadagi kabi shartnoma yuklang"
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