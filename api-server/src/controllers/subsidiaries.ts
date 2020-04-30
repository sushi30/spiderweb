import g from "../globals";
export async function getSubsidiaries(uuid: string) {
  const session1 = g.neo4j;
  const session2 = g.neo4j;
  const [nodes, edges] = await Promise.all([
    session1
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
      )
      .finally(() => session1.close()),
    session2
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
      )
      .finally(() => session2.close()),
  ]);
  return {
    nodes,
    edges,
  };
}
