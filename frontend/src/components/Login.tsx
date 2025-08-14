"use client";
import { useState } from "react";

interface Props {
  onLogin: (userId: string) => void;
}

export default function Login({ onLogin }: Props) {
  const [username, setUsername] = useState("");

  const handleLogin = async () => {
    if (!username) return;
    const res = await fetch("http://127.0.0.1:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    });
    const data = await res.json();
    onLogin(data.token);
  };

  return (
    <div className="container">
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Enter your username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
