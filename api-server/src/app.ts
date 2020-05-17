import express from "express";
import cors from "cors";
import errorHandler from "./middleware/errorHandler";
import requestLogger from "./middleware/requestLogger";
import v1 from "./v1";
import g from "./globals";

const app = express();

app.use(cors());
app.use(requestLogger());
app.use(express.json({}));
app.use(async (req, res, next) => g.init().then(() => next()));
app.use("/v1", v1);
app.use(errorHandler(Number.parseInt(process.env.DEBUG)));

export default app;
module.exports = app;
