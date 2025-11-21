import React, { useState } from 'react';
import { motion } from 'framer-motion';

const categories = [
    { id: 'math', name: 'Mathematics', icon: '📐', description: 'Research papers & complex concepts' },
    { id: 'tech', name: 'System Design', icon: '💻', description: 'Architecture & technical flows' },
    { id: 'startup', name: 'Startup Idea', icon: '🚀', description: 'Pitch decks & product concepts' },
];

const InputSection = ({ onGenerate }) => {
    const [selectedCategory, setSelectedCategory] = useState(categories[0].id);
    const [text, setText] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);

    const handleGenerate = () => {
        if (!text) return;
        setIsGenerating(true);
        onGenerate(text, selectedCategory);
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-6 space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {categories.map((cat) => (
                    <motion.div
                        key={cat.id}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setSelectedCategory(cat.id)}
                        className={`cursor-pointer p-6 rounded-xl border-2 transition-all ${selectedCategory === cat.id
                                ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/20'
                                : 'border-gray-700 bg-gray-800/50 hover:border-gray-600'
                            }`}
                    >
                        <div className="text-4xl mb-3">{cat.icon}</div>
                        <h3 className="text-xl font-bold text-white mb-1">{cat.name}</h3>
                        <p className="text-sm text-gray-400">{cat.description}</p>
                    </motion.div>
                ))}
            </div>

            <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
                <textarea
                    className="w-full h-40 bg-gray-900/50 border border-gray-700 rounded-lg p-4 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors resize-none"
                    placeholder="Paste your text, abstract, or idea here..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                />
                <div className="mt-4 flex justify-end">
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleGenerate}
                        disabled={isGenerating || !text}
                        className={`px-8 py-3 rounded-lg font-bold text-white shadow-lg ${isGenerating || !text
                                ? 'bg-gray-600 cursor-not-allowed'
                                : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:shadow-blue-500/25'
                            }`}
                    >
                        {isGenerating ? 'Generating...' : 'Generate Video'}
                    </motion.button>
                </div>
            </div>
        </div>
    );
};

export default InputSection;
