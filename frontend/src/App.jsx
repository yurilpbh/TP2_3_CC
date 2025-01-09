import React, { useState } from 'react';
import { SongInput } from './components/SongInput';
import { SongList } from './components/SongList';
import { RecommendationList } from './components/RecommendationList';
import { fetchRecommendations } from './services/api';

export default function App() {
  const [userSongs, setUserSongs] = useState([]);
  const [recommendationData, setRecommendationData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddSongs = async (newSongs) => {
    setUserSongs(newSongs);
    
    try {
      setLoading(true);
      setError(null);
      const data = await fetchRecommendations(newSongs);
      setRecommendationData({
        songs: data.songs,
        version: data.version,
        modelDate: data.model_date
      });
    } catch (err) {
      setError('Failed to fetch recommendations. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            Song Recommendations
          </h1>
        </div>

        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <SongInput onAddSongs={handleAddSongs} />
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}
          
          {loading && (
            <div className="mt-4 text-center text-gray-500">
              Loading recommendations...
            </div>
          )}
          
          <SongList 
            title="Your Songs" 
            songs={userSongs} 
          />
          
          {recommendationData && (
            <RecommendationList 
              recommendations={recommendationData.songs}
              version={recommendationData.version}
              modelDate={recommendationData.modelDate}
            />
          )}
        </div>
      </div>
    </div>
  );
}