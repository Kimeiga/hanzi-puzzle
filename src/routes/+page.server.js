// src/routes/api/generate-puzzle.js
import { generatePuzzle } from '$lib/generatePuzzle';

export async function load(params) {
    const puzzleData = await generatePuzzle();

    return puzzleData
}
