import React, { useState } from 'react';
import { parseSongList } from '../utils/songParser';

export function SongInput({ onAddSongs }) {
  const [songInput, setSongInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (songInput.trim()) {
      const songs = parseSongList(songInput);
      onAddSongs(songs);
      setSongInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="songInput" className="block text-sm font-medium text-gray-700">
          Enter Songs
        </label>
        <textarea
          id="songInput"
          value={songInput}
          onChange={(e) => setSongInput(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Enter songs separated by commas (e.g., I'm the One, T-Shirt, One Night)"
          rows={3}
        />
      </div>
      <button
        type="submit"
        className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      >
        Add Songs
      </button>
    </form>
  );
}