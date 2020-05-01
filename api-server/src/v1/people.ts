import * as express from "express";
import { getSubsidiariesGraph } from "../controllers/subsidiaries";
import { getPerson } from "../controllers/people";
import { expressAsyncWrapper as eaw } from "../express";
import { getDirectControl } from "../controllers/people";
import castResult from "../middleware/caseResult";
import { array, object } from "yup";
const router = express.Router();

router.get(
  "/:id/direct",
  eaw(async (req, res, next) => {
    const { id } = req.params;
    res.locals.result = await getDirectControl(id);
    if (!res.locals.result) {
      return res.status(404).end();
    }
    next();
  }),
  castResult(array().of(object().camelCase()))
);

router.get(
  "/:id/subsidiaries",
  eaw(async (req, res, next) => {
    const { id } = req.params;
    res.locals.result = await getSubsidiariesGraph(id);
    if (!res.locals.result) {
      return res.status(404).end();
    }
    next();
  }),
  castResult(array().of(object().camelCase()))
);

router.get(
  "/:id",
  eaw(async (req, res, next) => {
    const { id } = req.params;
    res.locals.result = await getPerson(id);
    if (!res.locals.result) {
      return res.status(404).end();
    }
    next();
  }),
  castResult(object().camelCase())
);

export default router;
