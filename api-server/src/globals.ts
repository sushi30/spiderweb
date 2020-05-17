import * as neo4j from "neo4j-driver";
import Neo4jPool from "./neo4j";

export default class Globals {
  static initialized = false;
  static neo4Pool = null;

  static validateInit() {
    if (!this.initialized) {
      throw Error("Globals haven't been initialized");
    }
  }

  static get neo4j() {
    this.validateInit();
    return this.neo4Pool;
  }

  static async init() {
    this.neo4Pool = new Neo4jPool(
      neo4j.driver("bolt://localhost:7687", neo4j.auth.basic("neo4j", "test"))
    );
    this.initialized = true;
  }
}
