import * as express from "express";
import { getSubsidiaries } from "../controllers/subsidiaries";
import { getPerson } from "../controllers/person";
import { expressAsyncWrapper as eaw } from "../express";
const router = express.Router();

router.get("/", (req, res) => {
  res.status(200).json({ message: "hello" });
});

router.get("/firms/:id", async (req, res) => {
  const { id } = req.params;
  const r = getPerson(id);
  if (!r) {
    res.status(404).end();
  }
  res.status(200).json(r);
});

router.get(
  "/person/:id",
  eaw(async (req, res) => {
    const { id } = req.params;
    const r = await getPerson(id);
    if (!r) {
      return res.status(404).end();
    }
    return res.status(200).json(r);
  })
);

router.get(
  "/person/:id/subsidiaries",
  eaw(async (req, res) => {
    const { id } = req.params;
    const r: any = await getSubsidiaries(id);
    res.status(200).json(r);
  })
);

export default router;
