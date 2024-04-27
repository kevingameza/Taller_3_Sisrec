import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import "../App.css";

function Home() {
  const [recommendedPlaces, setRecommendedPlaces] = useState(null);
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
          const placesWithDetails = await Promise.all(
            recommendations.map(async (recomendation) => {
              const placesResponse = await fetch(
                `http://127.0.0.1:8000/businesses/${recomendation.business_id}`
              );
              if (!placesResponse.ok) {
                throw new Error("Failed to fetch place details");
              }
              const placeDetails = await placesResponse.json();
              return { ...recomendation, title: placeDetails.name }; // Combine the recommendation and detailed information
            })
          );
          setRecommendedPlaces(placesWithDetails); // Aquí es donde deberíamos usar la variable correcta
        } catch (error) {
          console.error("Error fetching recommendations:", error);
          // Handle errors (display an error message to the user)
        }
      };

      fetchRecommendations();
    }
  }, [userId]); // Re-run useEffect when userId changes

  if (!recommendedPlaces) {
    return <div className="detail-view">Loading...</div>;
  }

  return (
    <div className="home-view">
      <img
        src="https://fineproxy.org/wp-content/uploads/2023/09/Yelp-for-Business-logo.png"
        alt="Yelp Logo"
        className="logo"
      />
      <h1>Recommended Businesses</h1>
      <div className="place-grid">
        {recommendedPlaces.map((place) => (
          <div className="place-card">
            <h3>{place.title}</h3>
            <Link
              to={`/places/${place.business_id}`}
              key={place.business_id}
              className="place-link"
            >
              See more
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
