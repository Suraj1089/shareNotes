import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import { PORT,HOST,DATABASE_URI } from "./apis/config";
import { socketIo } from "./apis/socket";

// initialize express app
const app: express.Application = express();

// create http server
const server = createServer(app);

// create socket io server
const io = new Server(server);

io.on('connection', (socket) => {
    console.log('a user connected');
    socketIo(socket);
  });
  

  server.listen(PORT, () => {
    console.log(`listening on *:${PORT}`);
  });

