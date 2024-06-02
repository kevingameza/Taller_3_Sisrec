import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import "../App.css";

function Home() {
  const [recommendedMovies, setRecommendedMovies] = useState(null);
  const userId = localStorage.getItem("userId"); // Get user ID from local storage

  useEffect(() => {
    if (userId) {
      const fetchRecommendations = async () => {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/recommendations/${userId}/`
          );
          if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
          }
          let recommendations = await response.json();

          if (recommendations.length === 0) {
            const response = await fetch(
              `http://127.0.0.1:8000/generate_top_n_recommendations/${userId}/`
            );
            if (!response.ok) {
              throw new Error("Failed to fetch recommendations");
            }
            recommendations = await response.json();
          }
          // Fetch additional information for each song
          const moviesWithDetails = await Promise.all(
            recommendations.map(async (recomendation) => {
              const moviesResponse = await fetch(
                `http://127.0.0.1:8000/movies/${recomendation.movie_id}`
              );
              if (!moviesResponse.ok) {
                throw new Error("Failed to fetch movie details");
              }
              const placeDetails = await moviesResponse.json();
              return { ...recomendation, title: placeDetails.name }; // Combine the recommendation and detailed information
            })
          );
          setRecommendedMovies(moviesWithDetails); // Aquí es donde deberíamos usar la variable correcta
        } catch (error) {
          console.error("Error fetching recommendations:", error);
          // Handle errors (display an error message to the user)
        }
      };

      fetchRecommendations();
    }
  }, [userId]); // Re-run useEffect when userId changes

  if (!recommendedMovies) {
    return <div className="detail-view">Loading...</div>;
  }

  return (
    <div className="home-view">
      <img
        src="https://seeklogo.com/images/I/imdb-logo-1CD1CCD432-seeklogo.com.png"
        alt="Imdb Logo"
        className="logo"
      />
      <h1>Recommended Movies</h1>
      <div className="movie-grid">
        {recommendedMovies.map((movie) => (
          <div className="movie-card">
            <h3>{movie.title}</h3>

            <Link
              to={`/movies/${movie.movie_id}`}
              key={movie.movie_id}
              className="movie-link"
            >
              <button type="submit" className="btn">
                See More
              </button>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
