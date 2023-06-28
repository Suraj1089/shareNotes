import { Socket } from "socket.io";
import { Server } from "socket.io";

export function socketIo(socket:Socket,io:Server) {
    socket.on('disconnect', () => {
        console.log(`user disconnected with id ${socket.id}`);
        // socket.to 
      });

      // sending chat message
      socket.on('chat',async (data:Object) => {
        /**
         * data = {
         *  user: User,
         *  chadId: UUID,
         *  message: String,
         *  Timestap: DATETIME
         * }
         */
        console.log(`socket id is ${socket.id} and data is ${data}`);
        io.emit('chat',data);
        
        
      });

      socket.on('end',async () => {
        console.log('end');//ws://localhost:3000
      })
}