import * as React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import { useIntl } from "react-intl";
import { Typography } from "@material-ui/core";

const useStyles = makeStyles({ table: {} });

interface Props {
  rows: any;
}

export default function DirectControlTable({ rows = [] }: Props) {
  const classes = useStyles();
  const getLocaleString = (id: string) =>
    useIntl().formatMessage({ id: `people.direct.${id}` });

  return (
    <React.Fragment>
      <Typography variant="h4">{getLocaleString("title")}</Typography>
      <TableContainer component={Paper}>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              <TableCell>{getLocaleString("columns.name")}</TableCell>
              <TableCell>{getLocaleString("columns.percent")}</TableCell>
              <TableCell>{getLocaleString("columns.numStocks")}</TableCell>
              <TableCell>{getLocaleString("columns.notes")}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row: any) => (
              <TableRow>
                <TableCell component="th">{row.name}</TableCell>
                <TableCell>{row.capitalPercent}</TableCell>
                <TableCell>{row.stockAmount}</TableCell>
                <TableCell>{row.notes}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </React.Fragment>
  );
}
