"use client";
import { useState } from "react";

interface Props {
  userId: string;
  onGenerated: (url: string) => void;
}

export default function TattooForm({ userId, onGenerated }: Props) {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt) return;
    setLoading(true);

    const res = await fetch("http://127.0.0.1:5000/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, user_id: userId }),
    });
    const data = await res.json();
    onGenerated(data.url);
    setLoading(false);
  };

  return (
    <div className="container">
      <h2>Generate Tattoo</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Describe your tattoo"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button type="submit">{loading ? "Generating..." : "Generate"}</button>
      </form>
    </div>
  );
}
