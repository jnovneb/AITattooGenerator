"use client";
import { useState } from "react";
import Login from "../components/Login";
import TattooForm from "../components/TattooForm";
import TattooResult from "../components/TattooResult";
import Gallery from "../components/Gallery";

export default function HomePage() {
  const [userId, setUserId] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!userId) return <Login onLogin={setUserId} />;

  return (
    <div>
      <TattooForm
        userId={userId}
        onGenerated={(url) => setImageUrl(url)}
      />
      <TattooResult imageUrl={imageUrl} loading={loading} />
      <Gallery userId={userId} />
    </div>
  );
}
