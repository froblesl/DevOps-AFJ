# Usa una imagen oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar Pipfile y Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Instalar pipenv y dependencias
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copiar el resto del código fuente
COPY . .

# Expone el puerto donde corre Flask
EXPOSE 5000

# Comando para ejecutar la app
CMD ["pipenv", "run", "python", "-m", "src.main"]
