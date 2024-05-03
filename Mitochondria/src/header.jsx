import React from "react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <img
        src="/logo.png"
        alt="Vita-AI Logo"
        style={{ height: 55, marginLeft: 80 }}
        wh
      />
      <span
        style={{
          fontFamily: "'Poppins', sans-serif",
          fontSize: 40,
          fontWeight: "bold",
          color: "#38B6FF",
          marginRight: 940,
          marginTop: 10,
        }}
      >
        Vita-AI
      </span>

      <div className="login" style={{ display: "flex", alignItems: "center" }}>
        <span
          style={{
            fontFamily: "'Poppins', sans-serif",
            fontWeight: "500",
            fontSize: 24,
            marginRight: 5,
          }}
        >
          Doctor?
          <Link
            to="/login"
            style={{
              fontFamily: "'Poppins', sans-serif",
              fontWeight: "500",
              fontSize: 24,
              marginRight: 5,
              marginLeft: 5,
              color: "#38B6FF",
            }}
          >
            Login
          </Link>
        </span>
        <span color="blue" style={{ marginRight: 90 }}>
          👤
        </span>
      </div>
    </header>
  );
}

export default Header;
