// components/Homepage.js
import React from 'react';
import './Homepage.css';
import mascotGif from '../images/sparkyAI.gif'; // Exact filename!

const Homepage = () => {
  return (
    <div className="homepage">
      <div className="main-content">
        <section className="mascot-container">
          <div className="mascot-image">
            <img src={mascotGif} alt="Sparky AI Mascot" />
          </div>
        </section>
        
        <section className="about-section">
          <h2>About Us</h2>
          <p>Welcome to SunHacks!</p>
          
          <div className="purpose-textbox">
            <h3>Our Purpose</h3>
            <p>
              Our project aims to revolutionize how students access and manage their academic resources through an AI-powered website.
            </p>
            <p>
              We understand that students often struggle with scattered information, limited support, and time management while navigating their educational journey.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Homepage;