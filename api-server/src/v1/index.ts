import * as express from "express";
import { getPerson } from "../controllers/people";
const router = express.Router();
import people from "./people";

router.use("/people", people);

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

export default router;
