import { Parameters } from "neo4j-driver/types/query-runner";
import { TransactionConfig } from "neo4j-driver/types/session";
import { Driver } from "neo4j-driver/types/driver";

export default class Neo4jPool {
  poolSize: number;
  driver: Driver;

  constructor(driver, poolSize = 10) {
    this.driver = driver;
  }

  async run(
    query: string,
    parameters?: Parameters,
    config?: TransactionConfig
  ) {
    const session = this.driver.session();
    try {
      return await session.run(query, parameters, config);
    } finally {
      await session.close();
      console.log("session closed");
    }
  }
}
