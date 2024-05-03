import React, { useState } from "react";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1
        style={{
          color: "#38b6ff",
          marginBottom: "20px",
          fontFamily: "'Poppins', sans-serif",
          fontSize: "50px",
          marginTop: "150px",
          fontWeight: "bold",
        }}
      >
        Doctor Login
      </h1>
      <form
        style={{
          display: "flex",
          flexDirection: "column",
          width: "300px",
          marginTop: "10px",
        }}
      >
        <input
          type="email"
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            fontFamily: "'Poppins', sans-serif",
            padding: "10px",
            marginBottom: "20px",
            border: "3px solid #38b6ff",
            borderRadius: "8px",
          }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            fontFamily: "'Poppins', sans-serif",
            padding: "10px",
            marginBottom: "30px",
            border: "3px solid #38b6ff",
            borderRadius: "8px",
          }}
        />
        <button
          onClick={(e) => {
            e.preventDefault();
            window.location.href = "https://docvisual.streamlit.app";
          }}
          style={{
            fontFamily: "'Poppins', sans-serif",
            backgroundColor: "#38b6ff",
            color: "white",
            padding: "12px 20px",
            border: "none",
            fontWeight: "bold",
            fontSize: "20px",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          Login
        </button>
      </form>
      <p style={{ marginTop: "15px" }}>
        Don't have an account?{" "}
        <a
          href="https://verfication.streamlit.app/"
          style={{ color: "#007bff", textDecoration: "none" }}
        >
          Sign up as a doctor
        </a>
      </p>
    </div>
  );
}

export default LoginPage;
