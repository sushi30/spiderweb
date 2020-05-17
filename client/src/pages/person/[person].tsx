import React from "react";
import Layout from "../../layouts/Person";
import { Promise } from "bluebird";
import fetch from "isomorphic-unfetch";
import path from "path";
import fs from "fs";

export default function Person({ direct, person }) {
  return <Layout data={{ direct: direct, person: person }} />;
}

export async function getStaticProps({ params }) {
  const { person: uuid } = params;
  return {
    props: await Promise.props({
      direct: fetch(
        `${process.env.BACKEND}/v1/people/${uuid}/direct`
      ).then((res) => res.json()),
      person: fetch(`${process.env.BACKEND}/v1/people/${uuid}`).then((res) =>
        res.json()
      ),
    }),
  };
}

export async function getStaticPaths() {
  const persons = JSON.parse(
    fs
      .readFileSync(path.join(process.cwd(), "static", "person.json"))
      .toString()
  );
  return {
    paths: persons.map((person) => ({
      params: {
        person,
      },
    })),
    fallback: false,
  };
}
