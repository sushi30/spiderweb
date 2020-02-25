import express from "express";
import cors from "cors";

import errorHandler from "./middleware/errorHandler";
import requestLogger from "./middleware/requestLogger";
import hello from "./root/hello";

const app = express();

const corsMiddleware = (domain: string) =>
  cors({
    allowedHeaders: "content-type, access_token, etag",
    origin: domain,
    credentials: true
  });

app.use(corsMiddleware(process.env.DOMAIN));
app.use(requestLogger());
app.use(express.json({}));
app.use("/v1/hello", hello);
app.use(errorHandler(Number.parseInt(process.env.DEBUG)));

export default app;
