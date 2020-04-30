import express from "express";
import cors from "cors";

import errorHandler from "./middleware/errorHandler";
import requestLogger from "./middleware/requestLogger";
import v1 from "./v1";

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
app.use("/v1", v1);
app.use(errorHandler(Number.parseInt(process.env.DEBUG)));

export default app;
