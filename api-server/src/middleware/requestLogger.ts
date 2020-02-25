import { Response, NextFunction, Request } from "express";

function requestLogger() {
  return (req: Request, res: Response, next: NextFunction) => {
    const { path, query, body, method } = req;
    console.info({ path, query, body, method });
    next();
  };
}

export default requestLogger;

module.exports = requestLogger;
