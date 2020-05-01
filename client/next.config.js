!["dev", "prod"].includes(process.env.ENV) && require("dotenv").config();

module.exports = {
  env: {
    BACKEND: process.env.BACKEND,
    ENV: process.env.ENV
  }
};
