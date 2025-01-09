import React from 'react';

export function RecommendationList({ recommendations, version, modelDate }) {
  if (!recommendations) {
    return null;
  }

  return (
    <div className="mt-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-medium text-gray-900">Recommended Songs</h2>
        <div className="text-sm text-gray-500">
          <p>Version: {version}</p>
          <p>Model Date: {modelDate}</p>
        </div>
      </div>
      
      {recommendations.length === 0 ? (
        <p className="text-gray-500">No recommendations available.</p>
      ) : (
        <ul className="divide-y divide-gray-200">
          {recommendations.map((song, index) => (
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