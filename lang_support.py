import os
from dotenv import load_dotenv
from euriai import EuriaiClient

load_dotenv()

api_key = os.getenv("EURI_API_KEY")
if not api_key:
    raise ValueError("❌ EURI_API_KEY not found in environment!")

client = EuriaiClient(
    api_key=api_key,
    model="gpt-4.1-nano"  # Or any other supported model
)

def generate_prompt(task: str, lang: str, text: str, title: str = ""):
    base_prompt = {
        "en": f"Summarize the chapter titled '{title}' in concise points for students.",
        "hi": f"इस अध्याय '{title}' को छात्रों के लिए संक्षेप में समझाइए।",
        "es": f"Resume el capítulo titulado '{title}' en puntos concisos para los estudiantes."
    }

    try:
        prompt = base_prompt.get(lang, base_prompt["en"]) + "\n\n" + text
        response = client.generate_completion(
            prompt=prompt,
            temperature=0.7,
            max_tokens=800
        )
        return response
    except Exception as e:
        print("💥 Error calling EURI API:", e)
        return "❌ Failed to generate summary from EURI."
