import React from "react";
import Paper from "@material-ui/core/Paper";
import CircularProgress from "@material-ui/core/CircularProgress";
import { DataGrid } from "@material-ui/data-grid";
import axios from "axios";

const EntrepreneurTable = () => {
  const [headers, setHeaders] = React.useState([]);
  const [rows, setRows] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  // run the API calls on first load
  React.useEffect(() => {
    axios
      .get("entrepreneur/variables/2016")
      .then(response => {
        const columns = response.data;
        setHeaders(columns);
        return axios.get(
          `entrepreneur/2016?headers=${columns
            .map(column => column.name)
            .join("&headers=")}`
        );
      })
      .then(response => {
        setRows(response.data.map((row, index) => ({ ...row, id: index })));
        setLoading(false);
      })
      .catch(err => console.error("unable to grab the table records", err));
  }, [setRows, setHeaders]);

  return (
    <div>
      <span>Characteristics of Business Owners</span>
      <Paper>
        <div style={{ height: "90vh", width: "90vw" }}>
          {loading ? (
            <CircularProgress />
          ) : (
            <DataGrid
              columns={headers.map(header => ({
                field: header.name,
                headerName: header.label
              }))}
              rows={rows}
            />
          )}
        </div>
      </Paper>
    </div>
  );
};

export default EntrepreneurTable;
