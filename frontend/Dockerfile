# pull official base image
FROM node:20

# set working directory
WORKDIR /home/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /home/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json ./
COPY package-lock.json ./
# RUN npm install
RUN npm ci

COPY src ./
COPY public ./

# start app
CMD ["npm", "start"]
