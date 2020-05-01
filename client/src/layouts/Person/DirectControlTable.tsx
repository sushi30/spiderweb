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

const useStyles = makeStyles({ table: {} });

interface Props {
  rows: any;
}

export default function DirectControlTable({ rows = [] }: Props) {
  const classes = useStyles();
  const getLocaleString = (id: string) =>
    useIntl().formatMessage({ id: `people.direct.${id}` });

  return (
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
            <TableRow key={row.name}>
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="right">{row.capitalPercent}</TableCell>
              <TableCell align="right">{row.fat}</TableCell>
              <TableCell align="right">{row.carbs}</TableCell>
              <TableCell align="right">{row.protein}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
