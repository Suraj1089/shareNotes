import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import { PORT,HOST,DATABASE_URI } from "./apis/config";

// initialize express app
const app: express.Application = express();

// create http server
const server = createServer(app);

// create socket io server
const io = new Server(server);

app.get('/', (req, res) => {
  res.send({
    data:" hello "
  })
})
io.on('connection', (socket) => {
    console.log('a user connected');
  });
  
  server.listen(PORT, () => {
    console.log('listening on *:3000');
  });

