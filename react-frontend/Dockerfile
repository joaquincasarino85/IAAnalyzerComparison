# Build stage
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
COPY . .
RUN npm install
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist ./dist
COPY start.sh .
RUN chmod +x start.sh
EXPOSE 8080
CMD ["./start.sh"]

