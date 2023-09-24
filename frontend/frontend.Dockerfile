# Use the official Node.js 14 image as the base image
FROM node:alpine

# Set the working directory inside the container
WORKDIR /frontend

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend code to the container
COPY . .

# Build the frontend code
RUN npm run build

# Expose the port that Vite serves on (default: 5173)
EXPOSE 5173

# Set the command to run the frontend server
CMD ["npm", "run", "serve"]
