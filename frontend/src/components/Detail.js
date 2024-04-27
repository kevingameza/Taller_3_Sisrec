import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useParams } from "react-router-dom"; // Importar useParams

import { faThumbsUp, faThumbsDown } from "@fortawesome/free-solid-svg-icons"; // Import specific icons
import MapComponent from "./Map";

import "./Detail.css"; // Import your styling
import "../App.css";

function Detail(props) {
  const [place, setPlace] = useState(null);
  const [selectedRating, setSelectedRating] = useState(null); // Track selected rating
  const { placeId } = useParams();

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const placeResponse = await fetch(
          `http://127.0.0.1:8000/businesses/${placeId}`
        );
        if (!placeResponse.ok) {
          throw new Error("Failed to fetch place details");
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

    if (!place || !place.id) {
      console.error(
        "Missing place data or ID to update recommendation status."
      );
      return; // Prevent sending request without place information
    }

    if (rating === null) {
      console.error("Missing rating.");
      return; // Prevent sending request without rating information
    }

    const response = await fetch(
      `http://127.0.0.1:8000/recommendations/${place.id}`,
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
        `Error updating recommendation status for song ${place.id}:`,
        await response.text()
      );
    } else {
      console.log(`Recommendation status updated for place ${place.id}`);
      // Optionally, update the place state locally if successful
      // setplace({ ...place, status: rating }); // Update place status in state
    }
  };

  if (!place) {
    return <div className="detail-view">Loading...</div>;
  }

  return (
    <div className="detail-view">
      <img
        src="https://fineproxy.org/wp-content/uploads/2023/09/Yelp-for-Business-logo.png"
        alt="Yelp Logo"
        className="logo"
      />
      <div className="info-container">
        <h1>{place.name}</h1>
        <h2>{place.address}</h2>
        <h3>Expected rating: {place.stars}</h3>

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
      <MapComponent latitude={place.latitude} longitude={place.longitude} />
    </div>
  );
}

export default Detail;
