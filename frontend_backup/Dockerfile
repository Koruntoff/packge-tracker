FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the project
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy built assets from build stage
COPY --from=build /app/dist ./dist  # Changed from 'build' to 'dist'
COPY --from=build /app/package*.json ./

# Install production dependencies only
RUN npm install --production

# Expose port
EXPOSE 3000

# Start the application
CMD ["node", "./dist/server/index.js"]  # Updated start command