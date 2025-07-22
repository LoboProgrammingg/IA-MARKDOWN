# Imagem base enxuta
FROM python:3.10-slim

# Cria usuário não-root
RUN useradd -m appuser

WORKDIR /app/IA-MARKDOWN

# Instala dependências primeiro para cache eficiente
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia só o necessário (ajuste conforme sua estrutura)
COPY . .

# Permissões para usuário não-root
RUN chown -R appuser:appuser /app/IA-MARKDOWN

USER appuser

EXPOSE 8000

# Por padrão, roda em modo produção (sem --reload)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Para desenvolvimento, sobrescreva o CMD no docker-compose:
# command: uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
