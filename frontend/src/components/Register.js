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
        body: JSON.stringify({ user_id:username, password: username }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }
 
      // Save user ID in local storage
      localStorage.setItem('userId', username);

      navigate('/home');
    } catch (error) {
      console.error('Registration error:', error);
      // Display an error message to the user
    }
  };

  return (
    <div className="register-container">
      <img src="https://seeklogo.com/images/I/imdb-logo-1CD1CCD432-seeklogo.com.png" alt="Imdb Logo" className="logo" />
      <h2>Register</h2>
      <form onSubmit={handleSubmit} className="register-form">
        <input
          type="user"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <button type="submit" className='btn'>Register</button>
      </form>
      <p>
        Already have an account?{' '}
        <Link to="/login" className="btn">
          Login
        </Link>
      </p>
    </div>
  );
}

export default Register;
