// Register.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Register.css';
import '../App.css';

function Register() {
  const [username, setUsername] = useState('');
  const navigate = useNavigate(); 
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, country: 'Colombia', password: username }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }
 
      const data = await response.json();

      // Save user ID in local storage
      localStorage.setItem('userId', data.id);

      navigate('/preferences');
    } catch (error) {
      console.error('Registration error:', error);
      // Display an error message to the user
    }
  };

  return (
    <div className="register-container">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lastfm_logo.svg/2560px-Lastfm_logo.svg.png" alt="Last.fm Logo" className="logo" />
      <h2>Register</h2>
      <form onSubmit={handleSubmit} className="register-form">
        <input
          type="user"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
      <p>
        Already have an account?{' '}
        <Link to="/login" className="register-link">
          Login
        </Link>
      </p>
    </div>
  );
}

export default Register;
