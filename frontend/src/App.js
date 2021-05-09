import React from "react";
import axios from "axios";

import EntrepreneurTable from './EntrepreneurTable'

import "./App.css";

// set all the axios defaults
axios.defaults.baseURL = process.env.REACT_APP_BACKEND_API_URL;
axios.defaults.headers.post["Content-Type"] = "application/json;charset=utf-8";
axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";

const App = () => {

  return (
    <div className="App">
      <header className="App-header">
        <EntrepreneurTable />
      </header>
    </div>
  );
};

export default App;
