import express from "express";
import dotenv from "dotenv";

// load dotenv
dotenv.config();

// constants
const PORT = process.env.PORT || 8000
const DATABASE_URL = process.env.DATABASE_URL || null
const HOST = process.env.HOST || "localhost"

const app: express.Application = express();


app.get('/',async (req:express.Request, res:express.Response) => {
    res.send({
        name: 'suraj',
        rollNo: 12
    })
})

app.listen(PORT, () => {
    console.log(`application running at http://${HOST}:${PORT}`);
})
