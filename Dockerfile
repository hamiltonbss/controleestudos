FROM python:3.9

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install -r requirements.txt

# Copiar o código da aplicação
COPY . /app/

# Expor a porta onde o Flask irá rodar
EXPOSE 5000

# Definir o comando para rodar a aplicação
CMD ["python", "run.py"]
