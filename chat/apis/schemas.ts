import mongoose, { Schema, mongo } from "mongoose";
import { v4 as uuidv4 } from 'uuid';


const userSchema = new mongoose.Schema({
    userId: Schema.Types.UUID,
    name: String,
    email: String,
    active: {
        type: Boolean,
        default: false
    }
});

// chat schema
const chatSchema = new mongoose.Schema({
    chatId: Schema.Types.UUID,
    senderId: String,
    receiverId: String,
    date: {
        type: Date,
        default: Date.now()
    }
})


const UserModel = mongoose.model('User', userSchema);
const ChatModel = mongoose.model('Chat',chatSchema);