FROM node:18-alpine

WORKDIR /app

# Install dependencies first
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source code
COPY . .

EXPOSE 5173

# Set host to 0.0.0.0 to allow external connections
ENV HOST=0.0.0.0

CMD ["sh", "-c", "npm run dev -- --host 0.0.0.0"]