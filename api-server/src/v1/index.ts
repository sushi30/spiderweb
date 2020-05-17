import * as express from "express";
import { getPerson } from "../controllers/people";
const router = express.Router();
import people from "./people";
import { searchByName } from "../controllers/search";
import castResult from "../middleware/caseResult";
import { array, mixed, object } from "yup";
import { expressAsyncWrapper as eaw } from "../express";

router.use("/people", people);

router.get("/", (req, res) => {
  res.status(200).json({ message: "hello" });
});

router.get(
  "/search",
  eaw(async (req, res, next) => {
    const { q } = req.query;
    res.locals.result = await searchByName(q);
    next();
  }),
  castResult(array().of(object().camelCase()))
);

router.get("/firms/:id", async (req, res) => {
  const { id } = req.params;
  const r = getPerson(id);
  if (!r) {
    res.status(404).end();
  }
  res.status(200).json(r);
});

export default router;
