import Container from "@material-ui/core/Container";
import React from "react";
import { Formik, Form, Field } from "formik";
import { TextField } from "formik-material-ui";
import { Button } from "@material-ui/core";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import CircularProgress from "@material-ui/core/CircularProgress";
import Link from "../../components/Link";

export interface Props {
  getResults: (query: string) => Promise<void>;
  results: any[] | null;
  loading: boolean;
}

export default function Layout({ getResults, results, loading }: Props) {
  return (
    <Container maxWidth="md">
      <Formik
        initialValues={{ query: "" }}
        onSubmit={({ query }) => getResults(query)}
      >
        {() => (
          <Form>
            <Field component={TextField} name="query" />
            <Button type="submit">Search</Button>
          </Form>
        )}
      </Formik>
      {loading && <CircularProgress />}
      {results && (
        <List>
          {results.map(({ name, type, uuid }) => (
            <ListItem>
              <ListItemText
                primary={<Link href={`/${type}/${uuid}`}>{name}</Link>}
              />
            </ListItem>
          ))}
        </List>
      )}
    </Container>
  );
}
