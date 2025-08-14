"use client";
import Loader from "./Loader";

interface Props {
  imageUrl: string | null;
  loading: boolean;
}

export default function TattooResult({ imageUrl, loading }: Props) {
  if (loading) return <Loader />;

  return (
    <div className="result-container">
      {imageUrl ? (
        <img src={imageUrl} alt="Generated Tattoo" className="tattoo-image" />
      ) : (
        <p className="no-image-text">Your tattoo will appear here.</p>
      )}
    </div>
  );
}
