/**
 * Parses a comma-separated string of songs into an array of song titles
 * @param {string} input - Comma-separated string of song titles
 * @returns {string[]} Array of cleaned song titles
 */
export function parseSongList(input) {
  return input
    .split(',')
    .map(song => song.trim())
    .filter(song => song.length > 0);
}