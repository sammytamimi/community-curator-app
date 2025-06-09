'use client';

import React, { useState } from 'react';
import { UpArrowIcon } from './icons';

export default function ChatInput() {
    const [message, setMessage] = useState('');

    const handleInput = (e: React.FormEvent<HTMLTextAreaElement>) => {
        const textarea = e.currentTarget;
        textarea.style.height = 'auto'; // Reset height to recalculate
        const scrollHeight = textarea.scrollHeight;
        textarea.style.height = `${scrollHeight}px`;
    };

    return (
        <div className="w-full max-w-3xl mx-auto px-4">
             <div className="relative bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl">
                 <textarea
                     rows={1}
                     className="w-full max-h-48 p-4 pr-14 bg-transparent border-none rounded-2xl focus:outline-none focus:ring-0 resize-none text-base text-black dark:text-white placeholder-gray-500"
                     placeholder="Send a message..."
                     value={message}
                     onChange={(e) => setMessage(e.target.value)}
                     onInput={handleInput}
                 />
                <div className="absolute bottom-3 right-4 flex items-center">
                     <button
                        type="submit"
                        className="bg-gray-800 dark:bg-gray-200 text-white dark:text-black w-8 h-8 flex items-center justify-center rounded-full disabled:opacity-50"
                        disabled={!message.trim()}
                    >
                        <UpArrowIcon />
                    </button>
                 </div>
             </div>
        </div>
    );
} 