import React from 'react';
import { Link } from 'react-router-dom';
import './Landing.css';
import '../App.css';

function Landing() {
  return (
    <div className="landing-page">
      <img src="https://fineproxy.org/wp-content/uploads/2023/09/Yelp-for-Business-logo.png" alt="Yelp Logo" className="logo" />
      <h1>Welcome to recommendations app</h1>
      <p>Discover new businesses!</p>
      <div className="buttons">
        <Link to="/login" className="btn">Login</Link>
      </div>
    </div>
  );
}


export default Landing;
