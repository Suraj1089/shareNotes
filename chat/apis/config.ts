import dotenv from "dotenv";

// load dotenv
dotenv.config();


export const PORT = process.env.PORT || 3000
export const DATABASE_URI = process.env.DATABASE_URI || "DATABASE"
export const HOST = process.env.HOST || "localhost"


