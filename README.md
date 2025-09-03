# 📧 Classificador de Emails – Backend (Python)

API responsável por processar emails, extrair texto de arquivos `.pdf`/`.txt`, enviar o conteúdo para a **OpenAI API (GPT-4o-mini)** e retornar a classificação + resposta sugerida.

---

## 🚀 Funcionalidades
- Recebe emails via POST (texto ou upload de arquivos).  
- Converte arquivos `.pdf` e `.txt` para texto puro.  
- Chama a **OpenAI API** para classificar:  
  - Retorna se o email é `produtivo` ou `improdutivo`;  
  - Sugere uma resposta automática.  
- Retorna o resultado em formato **JSON** para o frontend.

---

## 🛠️ Tecnologias
- **Python 3.10+**  
- **FastAPI**  
- **PyPDF2 (para ler PDFs)  
- **OpenAI Python SDK**  

---

## 📦 Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/classificador-emails-back.git
cd classificador-emails-back

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale dependências
pip install -r requirements.txt
```

---

## ▶️ Execução
```bash
uvicorn app:app --reload
```

A API ficará disponível em:
👉 `http://localhost:8000` (FastAPI)

---

## ⚙️ Configuração
Crie um arquivo `.env` com sua chave da OpenAI:

```
OPENAI_API_KEY=sua-chave-aqui
```

---

## ⌨️ Exemplo de resposta de classificação de texto
```json
{
  "categoria": "produtiva",
  "resposta_sugerida": "Obrigado pelo contato, vamos agendar uma reunião."
}
```

---
## 📄 Exemplo de resposta de classificação de arquivo
```json
{
  "categoria": "produtiva",
  "resposta_sugerida": "Obrigado pelo contato, vamos agendar uma reunião.",
  "texto_extraido": "Boa tarde. Gostaria de agendar uma reunião para repassar os dados do ultimo orçamento. Daniel, Gerente de Vendas."
}
```

---

## 📜 Licença
Distribuído sob a licença MIT.
