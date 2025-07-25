# Usa imagem Python oficial
FROM python:3.12-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Expõe a porta que Flask usará
EXPOSE 8080

# Comando para iniciar o servidor com SocketIO + eventlet
CMD ["python", "app.py"]
