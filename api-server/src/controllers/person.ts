import g from "../globals";
export async function getPerson(uuid: string) {
  const { neo4j } = g;
  return await neo4j
    .run("MATCH (f:Person) WHERE f.uuid={uuid} RETURN f", {
      uuid
    })
    .then(({ records }) => records?.[0]?._fields?.[0]?.properties)
    .finally(neo4j.close());
}
