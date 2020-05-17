import g from "../globals";

export async function getSubsidiariesGraph(uuid: string) {
  const { neo4j } = g;
  const [nodes, edges] = await Promise.all([
    neo4j
      .run(
        `
    MATCH (s:Person)
    WHERE s.uuid={uuid}
    RETURN s as f
    UNION ALL MATCH (s:Person)-[*]->(f)
    WHERE s.uuid={uuid}
    RETURN f`,
        {
          uuid,
        }
      )
      .then(
        ({ records }) =>
          records.map(({ _fields: [{ properties }] }) => properties) as any
      ),
    neo4j
      .run(
        `MATCH p=(s:Person)-[*]->(f) WHERE s.uuid={uuid}
      UNWIND relationships(p) as rel
      WITH collect(id(rel)) as rels
        MATCH (a)-[r]->(b)
        WHERE id(r) in rels
        RETURN {start: a.uuid, end: b.uuid, props: r}`,
        {
          uuid,
        }
      )
      .then(({ records }) =>
        records.map(({ _fields: [{ start, end, props: { properties } }] }) => ({
          start,
          end,
          properties,
        }))
      ),
  ]);
  return {
    nodes,
    edges,
  };
}
