import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

import "./Home.css";
import "../App.css";

function Home() {
  const [recommendedMovies, setRecommendedMovies] = useState(null);
  const userId = localStorage.getItem("userId"); // Get user ID from local storage

  const TMDB_API_KEY = "e9b4d5daf252366da95083e70569592e";
  const TMDB_BASE_URL = "https://api.themoviedb.org/3";
  const TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";

  useEffect(() => {
    if (userId) {
      const fetchRecommendations = async () => {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/recommendations/user/${userId}/`
          );
          if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
          }
          let recommendations = await response.json();

          // Fetch additional information for each song
          const moviesWithDetails = await Promise.all(
            recommendations.map(async (recomendation) => {
              const moviesResponse = await fetch(
                `http://127.0.0.1:8000/movies/${recomendation.movie_id}`
              );
              if (!moviesResponse.ok) {
                throw new Error("Failed to fetch movie details");
              }
              const movieDetails = await moviesResponse.json();
              // Fetch poster from TMDb
              const tmdbResponse = await axios.get(
                `${TMDB_BASE_URL}/search/movie`,
                {
                  params: {
                    api_key: TMDB_API_KEY,
                    query: movieDetails.title.replaceAll('_',' '),
                    year: movieDetails.year,
                  },
                }
              );
              const tmdbMovie = tmdbResponse.data.results[0];
              const posterUrl = tmdbMovie
                ? `${TMDB_IMAGE_BASE_URL}${tmdbMovie.poster_path}`
                : null;

              return {
                ...recomendation,
                ...movieDetails,
                poster_url: posterUrl,
              };
            })
          );
          setRecommendedMovies(null);
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
          <div className="movie-card" key={movie.movie_id}>
            <img
              src={movie.poster_url}
              alt={`${movie.title} Poster`}
              className="movie-poster"
            />
            <div className="movie-info">
              <h3>{movie.title.replaceAll('_',' ')}</h3>
              <p>{movie.startyear}</p>
              <Link to={`/movies/${movie.movie_id}`} className="movie-link">
                <button type="button" className="btn">
                  See More
                </button>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
