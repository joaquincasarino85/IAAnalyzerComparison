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

# Exponer el puerto usado por Vite
EXPOSE 5173

# Comando para correr Vite en modo desarrollo
CMD ["npm", "run", "dev"]

