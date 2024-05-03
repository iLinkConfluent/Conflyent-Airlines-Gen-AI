cd ./ReactWebApp
npm i
npm run build
cd ..
cp -r ./ReactWebApp/build ./SocketServer/build
cd ./SocketServer
npm i
node express_server.js