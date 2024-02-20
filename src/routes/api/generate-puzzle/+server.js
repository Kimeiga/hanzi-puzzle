// src/routes/your-route/+page.server.js
import { generatePuzzle } from '$lib/generatePuzzle';

export async function GET({ url }) {
    const puzzleData = await generatePuzzle();
    return new Response(JSON.stringify(puzzleData));
}
