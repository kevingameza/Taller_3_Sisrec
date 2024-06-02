// App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
// import Register from "./components/Register";
import Landing from "./components/Landing";
import Home from "./components/Home"
import Detail from "./components/Detail";
import Preferences from "./components/Preferences";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Landing/>} />
          <Route path="/login" element={<Login/>} />
          {/* <Route path="/register" element={<Register/>} /> */}
          <Route path="/home" element={<Home/>}/>
          <Route path="/movies/:placeId" element={<Detail/>}/>
          <Route path="/preferences" element={<Preferences/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
