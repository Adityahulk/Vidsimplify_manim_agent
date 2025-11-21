import React from 'react';

const VideoPlayer = ({ videoUrl }) => {
    if (!videoUrl) return null;

    return (
        <div className="w-full max-w-4xl mx-auto mt-8 p-6 bg-gray-800/50 rounded-xl border border-gray-700">
            <h2 className="text-2xl font-bold text-white mb-4">Generated Video</h2>
            <div className="aspect-video bg-black rounded-lg overflow-hidden shadow-2xl">
                <video
                    src={videoUrl}
                    controls
                    className="w-full h-full object-contain"
                />
            </div>
            <div className="mt-4 flex justify-end">
                <a
                    href={videoUrl}
                    download="generated_video.mp4"
                    className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
                >
                    Download Video
                </a>
            </div>
        </div>
    );
};

export default VideoPlayer;
