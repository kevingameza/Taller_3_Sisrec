import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useParams } from "react-router-dom"; // Importar useParams

import { faThumbsUp, faThumbsDown } from "@fortawesome/free-solid-svg-icons"; // Import specific icons

import "./Detail.css"; // Import your styling
import "../App.css";

function Detail(props) {
  const [movie, setPlace] = useState(null);
  const [selectedRating, setSelectedRating] = useState(null); // Track selected rating
  const { placeId } = useParams();

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const placeResponse = await fetch(
          `http://127.0.0.1:8000/movies/${placeId}`
        );
        if (!placeResponse.ok) {
          throw new Error("Failed to fetch movie details");
        }
        const placeDetails = await placeResponse.json();
        setPlace(placeDetails); // Aquí es donde deberíamos usar la variable correcta
      } catch (error) {
        console.error("Error fetching recommendations:", error);
        // Handle errors (display an error message to the user)
      }
    };

    fetchRecommendations();
  }, [placeId]); // Re-run useEffect when userId changes

  const handleRateSong = async (rating) => {
    setSelectedRating(rating === selectedRating ? null : rating); // Toggle rating

    if (!movie || !movie.id) {
      console.error(
        "Missing movie data or ID to update recommendation status."
      );
      return; // Prevent sending request without movie information
    }

    if (rating === null) {
      console.error("Missing rating.");
      return; // Prevent sending request without rating information
    }

    const response = await fetch(
      `http://127.0.0.1:8000/recommendations/${movie.id}`,
      {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          status: rating === "thumbsDown" ? "negative" : "positive",
        }), // Send the updated status
      }
    );

    if (!response.ok) {
      console.error(
        `Error updating recommendation status for song ${movie.id}:`,
        await response.text()
      );
    } else {
      console.log(`Recommendation status updated for movie ${movie.id}`);
      // Optionally, update the movie state locally if successful
      // setplace({ ...movie, status: rating }); // Update movie status in state
    }
  };

  if (!movie) {
    return <div className="detail-view">Loading...</div>;
  }

  return (
    <div className="detail-view">
      <img
        src="https://seeklogo.com/images/I/imdb-logo-1CD1CCD432-seeklogo.com.png"
        alt="Imdb Logo"
        className="logo"
      />
      <div className="info-container">
        <h1>{movie.name}</h1>
        <h2>{movie.address}</h2>
        <h3>Expected rating: {movie.stars}</h3>

        {/* Rating Widget */}
        <div className="rating-widget">
          <button
            type="button"
            className={`thumbs-up ${
              selectedRating === "thumbsUp" ? "selected" : ""
            }`}
            onClick={() => handleRateSong("thumbsUp")}
          >
            <i className="fas fa-thumbs-up">
              <FontAwesomeIcon icon={faThumbsUp} />
            </i>
          </button>
          <button
            type="button"
            className={`thumbs-down ${
              selectedRating === "thumbsDown" ? "selected" : ""
            }`}
            onClick={() => handleRateSong("thumbsDown")}
          >
            <i className="fas fa-thumbs-down">
              <FontAwesomeIcon icon={faThumbsDown} />{" "}
            </i>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Detail;
