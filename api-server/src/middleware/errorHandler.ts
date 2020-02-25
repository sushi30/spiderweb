import { Response, Request, NextFunction } from "express";

function errorHandler(debug) {
  return (
    err: Error & { meta: any },
    req: Request,
    res: Response,
    next: NextFunction
  ) => {
    if (debug) {
      console.error(err.stack);
      err.meta?.body?.error && console.error(err.meta.body.error);
      res.status(500).send(err.stack);
    } else {
      console.error(err);
      res.status(500).send("Server Side Error");
    }
  };
}

export default errorHandler;

module.exports = errorHandler;
