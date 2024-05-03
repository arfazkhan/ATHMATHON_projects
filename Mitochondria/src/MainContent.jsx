import React from "react";

function MainContent() {
  return (
    <main style={{ textAlign: "center" }}>
      <h1
        style={{
          fontFamily: "'Poppins', sans-serif",
          fontSize: 80,
          fontWeight: "bold",
          color: "#38B6FF",
          paddingTop: 69,
          marginBottom: 40,
        }}
      >
        How Are You Feeling Today?
      </h1>
      <p
        style={{
          fontFamily: "'Poppins', sans-serif",
          fontWeight: 700,
          fontSize: 32,

          marginLeft: 400,
          marginRight: 400,
          marginBottom: 80,
        }}
      >
        Welcome to Scancer, where cutting-edge technology meets compassionate
        care. Experience healthcare redefined.
      </p>
      <div
        className="buttons"
        style={{ display: "flex", justifyContent: "center", gap: 120 }}
      >
        {/* Styles for both buttons */}
        <a href="https://vita-ai.streamlit.app/">
          <button
            className="vita-ai"
            style={{
              backgroundColor: "#38B6FF",
              color: "white",
              fontFamily: "'Poppins', sans-serif",
              fontWeight: "bold",
              padding: "10px 45px",
              borderRadius: 16,
              border: "none",
              fontSize: 24,
              cursor: "pointer",
              marginright: 100,
            }}
          >
            Vita-AI
          </button>
        </a>

        <a
          href="https://button4scan.streamlit.app/"
          style={{ textDecoration: "none" }}
        >
          <button
            className="scanner"
            style={{
              backgroundColor: "#38B6FF",
              color: "white",
              fontFamily: "'Poppins', sans-serif",
              fontWeight: "bold",
              padding: "10px 45px",
              borderRadius: 16,
              border: "none",
              fontSize: 24,
              cursor: "pointer",
              marginLeft: 100,
            }}
          >
            Scancer
          </button>
        </a>
      </div>
      <div
        className="button-descriptions"
        style={{
          marginTop: 10,
          display: "flex",
          justifyContent: "center",
          gap: 230,
        }}
      >
        <span
          style={{
            fontSize: 17,
            fontFamily: "'Poppins', sans-serif",
            fontWeight: "bold",
          }}
        >
          AI doctor Assistant
        </span>
        <span
          style={{
            fontSize: 17,
            fontFamily: "'Poppins', sans-serif",
            fontWeight: "bold",
          }}
        >
          Diagnose Your Scan
        </span>
      </div>
    </main>
  );
}
export default MainContent;
