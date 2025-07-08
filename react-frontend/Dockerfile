FROM node:18
WORKDIR /app
COPY package*.json ./
COPY . .
RUN npm install
RUN npm install -g serve
COPY start-entry.sh .
RUN chmod +x start-entry.sh
EXPOSE 8080
EXPOSE 5173
CMD ["./start-entry.sh"]

