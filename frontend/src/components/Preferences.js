import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css"; // Import your styling
import "./Preferences.css";
import "../App.css";

function Preferences() {
  const [selectedSongs, setSelectedSongs] = useState([]);
  const [recommendedSongs, setRecommendedSongs] = useState([]);
  const [sendingInteractions, setSendingInteractions] = useState(false); // Track sending state
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch random songs from the endpoint
    fetch("http://127.0.0.1:8000/songs/random/")
      .then((response) => response.json())
      .then((data) => setRecommendedSongs(data))
      .catch((error) => console.error("Error fetching songs:", error));
  }, []);

  const handleSelectSong = (songId) => {
    const isSelected = selectedSongs.some(
      (selectedSong) => selectedSong === songId
    );
    setSelectedSongs(
      isSelected
        ? selectedSongs.filter((selectedSong) => selectedSong !== songId)
        : [...selectedSongs, songId]
    );
  };

  const handleSendInteractions = async () => {
    const userId = localStorage.getItem("userId"); // Get user ID from local storage

    if (!userId) {
      console.error("User ID not found in local storage");
      return; // Prevent sending request without user ID
    }

    setSendingInteractions(true); // Set sending state to indicate in-progress

    try {
      for (const songId of selectedSongs) {
        const interaction = {
          user_id: userId,
          item_id: songId,
          rating: 1, // Set rating to 1
        };

        const response = await fetch("http://127.0.0.1:8000/interactions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(interaction),
        });

        if (!response.ok) {
          console.error(
            "Error sending interaction for song:",
            songId,
            await response.text()
          );
          // Handle individual interaction errors (optional)
        }
      }
      console.log("Interactions sent successfully");
      navigate("/home");
    } catch (error) {
      console.error("Error sending interactions:", error);
    } finally {
      setSendingInteractions(false); // Reset sending state after completion or error
    }
  };

  return (
    <div className="home-view">
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Lastfm_logo.svg/2560px-Lastfm_logo.svg.png"
        alt="Last.fm Logo"
        className="logo"
      />

      <h1>Select Your Preferences</h1>

      <div className="song-grid">
        {recommendedSongs.map((song) => (
          <div
            key={song.id}
            className={`${
              selectedSongs.includes(song.id)
                ? "song-card-selected"
                : "song-card"
            }`}
            onClick={() => handleSelectSong(song.id)}
          >
            <h3>{song.title}</h3>

            <p>{song.artist}</p>
          </div>
        ))}
      </div>
      <button
        onClick={handleSendInteractions}
        disabled={selectedSongs.length === 0 || sendingInteractions}
        className="btn"
      >
        {sendingInteractions ? "Sending Preferences..." : "Save Preferences"}
      </button>
    </div>
  );
}

export default Preferences;
