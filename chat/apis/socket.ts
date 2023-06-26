import { Socket } from "socket.io";

export function socketIo(socket:Socket) {
    socket.on('disconnect', () => {
        console.log(`user disconnected with id ${socket.id}`);
        // socket.to 
      });

      // sending chat message
      socket.on('chat',async (data:JSON) => {
        /**
         * data = {
         *  user: User,
         *  chadId: UUID,
         *  message: String,
         *  Timestap: DATETIME
         * }
         */
        console.log(`socket id is ${socket.id}`);
        socket.to(socket.id).emit("chat",{deliverd: true});
        
      });

      socket.on('end',async () => {
        console.log('end');
      })
}