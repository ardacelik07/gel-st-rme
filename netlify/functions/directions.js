// Netlify Serverless Function: Google Maps Directions API proxy
// CORS ve API key güvenliği için backend'den çağrı yapıyoruz

const API_KEY = process.env.GOOGLE_MAPS_API_KEY || 'AIzaSyAKS4a9rCu2hRTebc2lHA9o24BthtqyLjc';

exports.handler = async (event) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  const origin = event.queryStringParameters?.origin;
  const destination = event.queryStringParameters?.destination;

  if (!origin || !destination) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'origin ve destination parametreleri gerekli' }),
    };
  }

  const apiUrl = `https://maps.googleapis.com/maps/api/directions/json?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}&key=${API_KEY}&language=tr&units=metric&mode=driving`;

  try {
    const response = await fetch(apiUrl);
    const data = await response.text();
    return {
      statusCode: 200,
      headers,
      body: data,
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: err.message }),
    };
  }
};
