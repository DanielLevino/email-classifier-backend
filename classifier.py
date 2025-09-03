import os
import json
import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI
import re
import io

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_file(file, filename: str) -> str:
    """Extrai texto de arquivos .txt ou .pdf"""
    print(f"[DEBUG] Iniciando extração do arquivo: {filename}")

    if filename.endswith(".txt"):
        try:
            if isinstance(file, bytes):
                text = file.decode("utf-8")
            else:
                text = file.read().decode("utf-8")

            print(f"[DEBUG] Texto extraído do TXT (tamanho={len(text)} chars)")
            return text
        except Exception as e:
            print(f"[ERRO] Falha ao ler TXT: {e}")
            raise


    elif filename.endswith(".pdf"):

        try:
            # transforma os bytes em "arquivo em memória"
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file))
            text = ""
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                print(f"[DEBUG] Página {i + 1} extraída (tamanho={len(page_text) if page_text else 0} chars)")
            print(f"[DEBUG] Texto total extraído do PDF (tamanho={len(text)} chars)")

            return text

        except Exception as e:

            print(f"[ERRO] Falha ao ler PDF: {e}")

            raise
    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")


def classify_email(texto: str) -> tuple[str, str]:
    """Usa OpenAI GPT para classificar e gerar resposta"""
    print("[DEBUG] Iniciando classificação...")
    print(f"[DEBUG] Texto recebido (primeiros 200 chars): {texto[:200]}")

    prompt = f"""
    Você é um assistente que classifica emails em duas categorias: Produtivo ou Improdutivo.

    Email:
    \"\"\"{texto}\"\"\"

    Responda APENAS em JSON no seguinte formato:
    {{
      "categoria": "Produtivo" ou "Improdutivo",
      "resposta": "Texto da resposta automática"
    }}
    """

    try:
        print("[DEBUG] Enviando prompt para OpenAI...")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        print("[DEBUG] Resposta recebida da OpenAI.")
        content = resp.choices[0].message.content.strip()
        print(f"[DEBUG] Conteúdo bruto recebido:\n{content}")

        content = re.sub(r"^```json\s*|\s*```$", "", content, flags=re.MULTILINE).strip()

        print(f"[DEBUG] Conteúdo após limpeza:\n{content}")

        data = json.loads(content)
        print(f"[DEBUG] JSON parseado com sucesso: {data}")
        return data["categoria"], data["resposta"]

    except json.JSONDecodeError as e:
        print(f"[ERRO] Falha ao decodificar JSON: {e}")
        print("[ERRO] Conteúdo recebido não era JSON válido:")
        print(content)
        return "Indefinido", f"Erro ao processar JSON: {str(e)}"

    except Exception as e:
        print(f"[ERRO] Erro inesperado: {e}")
        return "Indefinido", f"Erro ao processar: {str(e)}"