import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

def get_financial_advice(total_savings, avg_savings_per_month, predicted_savings):
    """Send financial data to Google Gemini API and return personalized advice."""

    prompt = f"""
    Аз съм финансов консултант. Потребителят има следните финансови показатели:
    - Общо спестявания: ${total_savings}
    - Средни месечни спестявания: ${avg_savings_per_month}
    - Прогнозни спестявания за следващия месец: ${predicted_savings}

    Дай ми персонализиран финансов съвет как мога да подобря спестяванията си и да намаля ненужните разходи.
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text.strip() if response.text else "Не успях да генерирам съвет."
