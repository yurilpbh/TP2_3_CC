/**
 * API service for song recommendations
 */
export async function fetchRecommendations(songs) {
  try {
    const response = await fetch('http://127.0.0.1:52064/get_recommendation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ songs }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
}