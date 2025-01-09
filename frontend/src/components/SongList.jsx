import React from 'react';

export function SongList({ songs, title }) {
  return (
    <div className="mt-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">{title}</h2>
      {songs.length === 0 ? (
        <p className="text-gray-500">No songs added yet.</p>
      ) : (
        <ul className="divide-y divide-gray-200">
          {songs.map((song, index) => (
            <li key={index} className="py-4">
              <div className="flex space-x-3">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{song}</p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}