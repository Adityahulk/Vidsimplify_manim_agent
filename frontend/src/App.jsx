import React, { useState } from 'react';
import InputSection from './components/InputSection';
import VideoPlayer from './components/VideoPlayer';

function App() {
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (text, category) => {
    setLoading(true);
    setVideoUrl(null);
    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, category }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate video');
      }

      const data = await response.json();
      if (data.status === 'success') {
        setVideoUrl(data.video_url);
      } else {
        throw new Error('Generation failed');
      }
    } catch (error) {
      console.error("Error generating video:", error);
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans selection:bg-blue-500/30">
      <header className="p-6 border-b border-gray-800 bg-gray-900/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center font-bold text-xl">
              V
            </div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
              Vidsimplify
            </h1>
          </div>
          <div className="text-sm text-gray-400">
            AI-Powered Explainer Videos
          </div>
        </div>
      </header>

      <main className="py-12 px-4">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            Turn Ideas into Motion
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Create professional animated explainer videos from text, research papers, or startup ideas in seconds.
          </p>
        </div>

        <InputSection onGenerate={handleGenerate} />

        {loading && (
          <div className="text-center mt-8 text-gray-400 animate-pulse">
            Generating your masterpiece...
          </div>
        )}

        <VideoPlayer videoUrl={videoUrl} />
      </main>
    </div>
  );
}

export default App;
