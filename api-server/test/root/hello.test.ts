import request from "supertest";
import hello from "../../src/app";

describe("Test Hello", () => {
  it("should create a new post", async () => {
    const res = await request(hello)
      .get("/v1/hello")
      .send();
    expect(res.statusCode).toEqual(200);
    expect(res.body).toHaveProperty("message");
  });
});
