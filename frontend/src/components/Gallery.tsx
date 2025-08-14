"use client";
import { useEffect, useState } from "react";

interface ImageData {
  url: string;
  prompt: string;
}

interface Props {
  userId: string;
}

export default function Gallery({ userId }: Props) {
  const [images, setImages] = useState<ImageData[]>([]);

  useEffect(() => {
    async function fetchImages() {
      const res = await fetch(`http://127.0.0.1:5000/api/my-images?user_id=${userId}`);
      const data = await res.json();
      setImages(data);
    }
    fetchImages();
  }, [userId]);

  return (
    <div className="container">
      <h2>Your Previous Tattoos</h2>
      <div className="gallery">
        {images.map((img, idx) => (
          <img key={idx} src={img.url} alt={img.prompt} />
        ))}
      </div>
    </div>
  );
}
