export const config = {
  runtime: 'edge',
};

export default async function handler(request) {
  if (request.method === 'POST') {
    try {
      const data = await request.json();
      console.log('Feedback received:', data);
      
      // In a real app, save to DB here.
      // For now, we just log it.
      
      return new Response(JSON.stringify({ status: 'success' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    } catch (error) {
      return new Response(JSON.stringify({ status: 'error', message: 'Invalid JSON' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }
  }

  return new Response(JSON.stringify({ status: 'error', message: 'Method not allowed' }), {
    status: 405,
    headers: { 'Content-Type': 'application/json' },
  });
}
