import g from "../globals";

export async function getPerson(personUuid: string) {
  const { neo4j } = g;
  return await neo4j
    .run("MATCH (f:Person) WHERE f.uuid={uuid} RETURN f", {
      uuid: personUuid,
    })
    .then(({ records }) => records?.[0]?._fields?.[0]?.properties);
}

export async function getDirectControl(personUuid: string) {
  const { neo4j } = g;
  return await neo4j
    .run("MATCH (p:Person)-[r]->(f) WHERE p.uuid={uuid} RETURN f, r", {
      uuid: personUuid,
    })
    .then(
      ({ records }) =>
        records.map(({ _fields: [{ properties }, { properties: p2 }] }) => ({
          ...properties,
          ...p2,
        })) as any
    );
}
