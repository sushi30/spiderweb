import React from "react";
import useSWR from "swr";
import { useRouter } from "next/router";
import Layout from "../../layouts/Person";

function useData(uuid: string) {
  const direct = useSWR(`/v1/people/${uuid}/direct`, (url) =>
    fetch(process.env.BACKEND + url).then((res) => res.json())
  );
  const person = useSWR(`/v1/people/${uuid}`, (url) =>
    fetch(process.env.BACKEND + url).then((res) => res.json())
  );
  return { direct, person };
}

export default function Person() {
  const { person: uuid } = useRouter().query;

  const { direct, person } = useData(uuid as string);

  return direct.error ? (
    <div>{direct.error.message}</div>
  ) : direct.data && person.data ? (
    <Layout data={{ direct: direct.data, person: person.data }} />
  ) : (
    <div>loading</div>
  );
}
