import mongoose from "mongoose";
import { DATABASE_URI } from './config'

async function mongoClient() {
    await mongoose.connect(DATABASE_URI);
}