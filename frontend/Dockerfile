FROM node:18-alpine

WORKDIR /app

# Install dependencies first
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Install vite globally
RUN npm install -g vite

# Copy project files
COPY . .

EXPOSE 5173

# Use npx to run vite
CMD ["npx", "vite", "--host"]