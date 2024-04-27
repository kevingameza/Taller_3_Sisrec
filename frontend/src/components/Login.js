// Login.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
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
        src="https://fineproxy.org/wp-content/uploads/2023/09/Yelp-for-Business-logo.png"
        alt="Yelp Logo"
        className="logo"
      />
      <h2 style={{color: "black"}}>Login</h2>
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
    </div>
  );
}

export default Login;
