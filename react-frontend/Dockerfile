FROM node:20-alpine

# Crear y usar directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar todas las dependencias, incluyendo Vite
RUN npm install

# Asegurar que los binarios locales (como vite) estén en el PATH
ENV PATH /app/node_modules/.bin:$PATH

# Copiar el resto del código
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Exponer el puerto (Railway asignará el puerto dinámicamente)
EXPOSE 3000

# Comando para servir la aplicación construida
CMD ["sh", "-c", "vite preview --host 0.0.0.0 --port $PORT"]

