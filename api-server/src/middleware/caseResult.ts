import { Request, Response } from "express";

function castResult(schema, statusCode = 200) {
  return (req: Request, res: Response) => {
    return res.status(statusCode).json(schema.cast(res.locals.result));
  };
}

export default castResult;
