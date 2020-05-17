import React from "react";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import ProTip from "../components/ProTip";
import Link from "../components/Link";
import Copyright from "../components/Copyright";
import fetch from "isomorphic-unfetch";
import fs from "fs";
import path from "path";
import { List, ListItem, ListItemText } from "@material-ui/core";

interface Props {
  data: { name: string; uuid: string }[];
}

export default function Index({ data }: Props) {
  data.sort((a, b) => (a.name > b.name ? 1 : -1));
  return (
    <Container maxWidth="md">
      <List>
        {data.map(({ name, uuid }) => (
          <ListItem>
            <Link href={`/person/${uuid}`}>
              <ListItemText primary={name} />
            </Link>
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export async function getStaticProps() {
  const ids = JSON.parse(
    fs
      .readFileSync(path.join(process.cwd(), "static", "person.json"))
      .toString()
  );
  return {
    props: {
      data: await Promise.all(
        ids.map(async (uuid) => ({
          name: await fetch(`${process.env.BACKEND}/v1/people/${uuid}`)
            .then((res) => res.json())
            .then(({ name }) => name),
          uuid,
        }))
      ),
    },
  };
}
