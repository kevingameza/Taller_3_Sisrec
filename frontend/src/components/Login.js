// Login.js
import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import "./Login.css";
import "../App.css";

function Login() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate(); 

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: username,
          password: username,
          name: username,
        }),
      });

      if (!response.ok) {
        throw new Error("Registration failed");
      }

      const data = await response.json();

      // Save user ID in local storage
      localStorage.setItem("userId", data.user_id);

      navigate("/home");
    } catch (error) {
      console.error("Registration error:", error);
      // Display an error message to the user
    }
  };

  return (
    <div className="login-container">
      <img
        src="https://seeklogo.com/images/I/imdb-logo-1CD1CCD432-seeklogo.com.png"
        alt="Imdb Logo"
        className="logo"
      />
      <h2 style={{color: "white"}}>Login</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="user"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <button type="submit" className="btn">
          Login
        </button>

      </form>
      <p>
        Don't have an account?{" "}
        <Link to="/register" className="btn">
          Register
        </Link>
      </p>
    </div>
  );
}

export default Login;
