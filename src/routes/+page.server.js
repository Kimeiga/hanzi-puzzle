export const prerender = false;
import { generatePuzzle } from '$lib/generatePuzzle';

export async function load(params) {
    const puzzleData = await generatePuzzle();

    return puzzleData
}
