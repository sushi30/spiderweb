import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import DirectControlTable from "./DirectControlTable";
import React from "react";

export interface Props {
  data: any;
}

export default function Layout({ data }: Props) {
  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        {data.person.name}
      </Typography>
      <DirectControlTable rows={data.direct} />
    </Container>
  );
}
