import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useParams, Link } from "react-router-dom";
import { faThumbsUp, faThumbsDown } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

import "./Detail.css";
import "../App.css";

const TMDB_API_KEY = "e9b4d5daf252366da95083e70569592e";
const TMDB_BASE_URL = "https://api.themoviedb.org/3";
const TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";
const TMDB_LOGO_BASE_URL = "https://image.tmdb.org/t/p/original"; // Base URL for provider logos

function Detail(props) {
  const userId = localStorage.getItem("userId"); // Get user ID from local storage
  const [movie, setMovie] = useState(null);
  const [recommendedMovies, setRecommendedMovies] = useState(null);
  const [selectedRating, setSelectedRating] = useState(null);
  const [streamingProviders, setStreamingProviders] = useState([]);
  const { movieId } = useParams();

  useEffect(() => {
    const fetchMovieDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/movies/${movieId}`);
        if (!response.ok) {
          throw new Error("Failed to fetch movie details");
        }
        const movieDetails = await response.json();

        // Fetch poster from TMDb
        const tmdbResponse = await axios.get(`${TMDB_BASE_URL}/search/movie`, {
          params: {
            api_key: TMDB_API_KEY,
            query: movieDetails.title.replaceAll("_", " "),
            year: movieDetails.year,
          },
        });
        const tmdbMovie = tmdbResponse.data.results[0];
        const posterUrl = tmdbMovie
          ? `${TMDB_IMAGE_BASE_URL}${tmdbMovie.poster_path}`
          : null;

        setMovie({ ...movieDetails, poster_url: posterUrl });

        // Fetch streaming providers
        if (tmdbMovie) {
          const providersResponse = await axios.get(
            `${TMDB_BASE_URL}/movie/${tmdbMovie.id}/watch/providers`,
            {
              params: { api_key: TMDB_API_KEY },
            }
          );
          const providers = providersResponse.data.results.CO?.flatrate || [];
          setStreamingProviders(providers);
        }
      } catch (error) {
        console.error("Error fetching movie details:", error);
      }
    };

    fetchMovieDetails();
  }, [movieId]);

  useEffect(() => {
    if (userId) {
      const fetchRecommendedMovies = async () => {
        setRecommendedMovies(null);
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/recommendations/user/graph/${userId}/?movie_name=${movie.title.replaceAll(
              "_",
              " "
            )}`
          );
          if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
          }
          const recommendations = await response.json();

          const moviesWithDetails = await Promise.all(
            recommendations.slice(0, 5).map(async (recommendation) => {
              const movieResponse = await fetch(
                `http://127.0.0.1:8000/movies/${recommendation.movie_id}`
              );
              if (!movieResponse.ok) {
                throw new Error("Failed to fetch movie details");
              }
              const movieDetails = await movieResponse.json();

              const tmdbResponse = await axios.get(
                `${TMDB_BASE_URL}/search/movie`,
                {
                  params: {
                    api_key: TMDB_API_KEY,
                    query: movieDetails.title,
                    year: movieDetails.year,
                  },
                }
              );
              const tmdbMovie = tmdbResponse.data.results[0];
              const posterUrl = tmdbMovie
                ? `${TMDB_IMAGE_BASE_URL}${tmdbMovie.poster_path}`
                : null;

              return {
                ...recommendation,
                ...movieDetails,
                poster_url: posterUrl,
              };
            })
          );
          setRecommendedMovies(moviesWithDetails);
        } catch (error) {
          console.error("Error fetching recommendations:", error);
        }
      };

      fetchRecommendedMovies();
    }
  }, [userId, movie]);

  const handleRateMovie = async (rating) => {
    setSelectedRating(rating === selectedRating ? null : rating); // Toggle rating

    if (!movie || !movie.id) {
      console.error(
        "Missing movie data or ID to update recommendation status."
      );
      return;
    }

    if (rating === null) {
      console.error("Missing rating.");
      return;
    }

    const response = await fetch(
      `http://127.0.0.1:8000/recommendations/${movie.id}`,
      {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          status: rating === "thumbsDown" ? "negative" : "positive",
        }),
      }
    );

    if (!response.ok) {
      console.error(
        `Error updating recommendation status for movie ${movie.id}:`,
        await response.text()
      );
    } else {
      console.log(`Recommendation status updated for movie ${movie.id}`);
    }
  };

  if (!movie) {
    return <div className="detail-view">Loading...</div>;
  }

  return (
    <div className="detail-view">
      <div className="top-bar">
        <Link to="/home" className="home-button">
          <button type="button" className="btn">
            Home
          </button>
        </Link>
      </div>
      <img
        src="https://seeklogo.com/images/I/imdb-logo-1CD1CCD432-seeklogo.com.png"
        alt="Imdb Logo"
        className="logo"
      />
      <div className="info-container">
        <img
          src={movie.poster_url}
          alt={`${movie.title} Poster`}
          className="movie-poster"
        />
        <div className="movie-details">
          <h1>{movie.title.replaceAll("_", " ")}</h1>
          {movie.year && <h3>Year: {movie.year}</h3>}
          {movie.isAdult !== null && (
            <p>{movie.isAdult ? "Adults Only" : "All Ages"}</p>
          )}
          <h2>Genre:</h2>
          <ul>
            {movie.genres.split("|").map((genre, index) => (
              <li key={index}>{genre}</li>
            ))}
          </ul>
          <div className="rating-widget">
            <button
              type="button"
              className={`thumbs-up ${
                selectedRating === "thumbsUp" ? "selected" : ""
              }`}
              onClick={() => handleRateMovie("thumbsUp")}
            >
              <FontAwesomeIcon icon={faThumbsUp} />
            </button>
            <button
              type="button"
              className={`thumbs-down ${
                selectedRating === "thumbsDown" ? "selected" : ""
              }`}
              onClick={() => handleRateMovie("thumbsDown")}
            >
              <FontAwesomeIcon icon={faThumbsDown} />
            </button>
          </div>
          <div className="streaming-providers">
            <h2>Available to stream in Colombia:</h2>
            {streamingProviders.length > 0 ? (
              <div className="provider-logos">
                {streamingProviders.map((provider, index) => (
                  <img
                    key={index}
                    src={`${TMDB_LOGO_BASE_URL}${provider.logo_path}`}
                    alt={provider.provider_name}
                    className="provider-logo"
                  />
                ))}
              </div>
            ) : (
              <p>No streaming providers available</p>
            )}
          </div>
        </div>
      </div>
      {recommendedMovies ? (
        <div className="recommended-movies">
          <h2>Similar Movies</h2>
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
      ):<div className="detail-view">Loading similar movies...</div>}
    </div>
  );
}

export default Detail;
