import g from "../globals";

export async function searchByName(query: string) {
  const { neo4j } = g;
  const people = await neo4j
    .run(
      `MATCH (p:Person)
    WHERE replace(replace(p.name, '"', ''), ".", "") contains {query}
    RETURN p`,
      {
        query,
      }
    )
    .then(
      ({ records }) =>
        records.map(({ _fields: [{ properties }] }) => ({
          ...properties,
          type: "person",
        })) as any
    )
    .then((res) => res.sort((a, b) => (a.name > b.name ? 1 : -1)));
  const firms = await neo4j
    .run(
      `MATCH (p:Firm)
    WHERE replace(replace(p.name, '"', ''), ".", "") contains {query}
    RETURN p`,
      {
        query,
      }
    )
    .then(
      ({ records }) =>
        records.map(({ _fields: [{ properties }] }) => ({
          ...properties,
          type: "firm",
        })) as any
    )
    .then((res) => res.sort((a, b) => (a.name > b.name ? 1 : -1)));
  return [...people, ...firms];
}
