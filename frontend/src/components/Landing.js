import React from 'react';
import { Link } from 'react-router-dom';
import './Landing.css';
import '../App.css';

function Landing() {
  return (
    <div className="landing-page">
      <img src="https://seeklogo.com/images/I/imdb-logo-1CD1CCD432-seeklogo.com.png" alt="Imdb Logo" className="logo" />
      <h1>Welcome to your movies recommendator app</h1>
      <p>Discover new movies and new worlds!</p>
      <div className="buttons">
        <Link to="/login" className="btn">Login</Link>
        <Link to="/register" className="btn">Register</Link>
      </div>
    </div>
  );
}


export default Landing;
