import { Socket } from "socket.io";

export function socketIo(socket:Socket) {
    socket.on('disconnect', () => {
        console.log('user disconnected');
      });

      socket.on('data',async (data:string) => {
        console.log('data')
      });

      socket.on('end',async () => {
        console.log('end')
      })
}