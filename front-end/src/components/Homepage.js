// components/Homepage.js
import React from 'react';
import './Homepage.css';
import mascotGif from '../images/sparkyemotes.gif';

const Homepage = () => {
  return (
    <div className="homepage">
      <div className="main-content">
        <section className="mascot-container">
          {/* Text above the mascot */}
          <div className="mascot-text-above">
            <h3>Meet our mascot, Sparky.AI!</h3>
          </div>
          
          {/* Mascot image */}
          <div className="mascot-image">
            <img src={mascotGif} alt="Sparky AI Mascot" />
          </div>
          
          {/* Text below the mascot */}
          <div className="mascot-text-below">
            <p>He loves helping fellow sundevils and those around him!</p>
          </div>
        </section>
        
        <section className="about-section">
          <h2>About Us</h2>
          <p>Welcome to our team project! Our team, T.I.L.T, is here to help make ASU's resources more accessible to you! Enjoy! :'D</p>
          
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