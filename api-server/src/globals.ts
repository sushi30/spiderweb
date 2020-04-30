import * as neo4j from "neo4j-driver";

export default class Globals {
  static initialized = false;
  static neo4Driver = null;

  static validateInit() {
    if (!this.initialized) {
      throw Error("Globals haven't been initialized");
    }
  }

  static get neo4j() {
    this.validateInit();
    return this.neo4Driver.session();
  }

  static async init() {
    this.neo4Driver = neo4j.driver(
      "bolt://localhost:7687",
      neo4j.auth.basic("neo4j", "test")
    );
    this.initialized = true;
  }
}
