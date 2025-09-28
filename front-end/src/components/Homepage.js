// components/Homepage.js
import React from 'react';
import './Homepage.css';

const Homepage = () => {
  return (
    <div className="homepage">
      <div className="main-content">
        <section className="mascot-container">
          <div className="mascot-placeholder">
            <p>Mascot Image Placeholder</p>
            <p>Replace with your mascot image</p>
          </div>
        </section>
        
        <section className="about-section">
          <h2>About Us</h2>
          <p>Welcome to SunHacks! We are dedicated to creating innovative solutions that make a difference in our community.</p>
          
          <div className="purpose-textbox">
            <h3>Our Purpose</h3>
            <p>
              This is where you can describe the purpose of your project. Explain what your company does, 
              what problems you solve, and what makes your approach unique. You can edit this text directly 
              in the component to customize it for your specific needs.
            </p>
            <p>
              Feel free to expand on your mission, vision, and values. This section is fully customizable 
              to reflect your organization's goals and aspirations. Our team is committed to excellence 
              and innovation in everything we do.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Homepage;