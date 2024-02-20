
// import the data 

import { promises as fs } from 'fs';
import path from 'path';

async function loadData(p) {
    const filePath = path.resolve(p);
    const jsonData = JSON.parse(await fs.readFile(filePath, 'utf8'));
    return jsonData;
}

const numberOfComponents = 9;

function getRandomKeyValuePair(obj) {
    const keys = Object.keys(obj);
    const randomKey = keys[Math.floor(Math.random() * keys.length)];
    const randomValue = obj[randomKey];
    return [randomKey, randomValue];
}

export async function generatePuzzle() {
    const charData = await loadData('src/lib/data/new/char2wordContainingChar_min.json');
    const strokeNumber2Component = await loadData('src/lib/data/all_components.json');

    // get random character from charData

    const [char, randomChar] = getRandomKeyValuePair(charData);

    // // get 9 random components from strokeNumber2Component, with duplicates
    // for (let i = 0; i < numberOfComponents; i++) {
    //     const randomIndex = Math.floor(Math.random() * strokeNumber2Component.length);
    //     randomComponents.push(strokeNumber2Component[randomIndex]);
    // }

    const randomComponents = [];
    // console.log(randomChar)
    // console.log(randomChar.ids)
    // console.log(randomChar.ids.length)
    // console.log(randomChar.ids_strokes)

    for (let i = 0; i < numberOfComponents - randomChar.i.length; i++) {
        const indexOfComponentToConsider = i % randomChar.s.length;
        const componentToConsider = randomChar.s[indexOfComponentToConsider];

        // console.log(randomChar.ids_strokes)
        // console.log(strokeNumber2Component[randomChar.ids_strokes[i % randomChar.ids_strokes.length]])
        // console.log(strokeNumber2Component[randomChar.ids_strokes[i % randomChar.ids_strokes.length]].length)

        // if (!(randomChar.ids_strokes[indexOfComponentToConsider] in strokeNumber2Component)) {
        //     console.log(`${randomChar.ids_strokes[i % randomChar.ids_strokes.length]} not found in strokeNumber2Component`);
        //     // Optionally, continue to the next iteration or perform other logic
        //     continue;
        // }

        const randomIndex = Math.floor(Math.random() * strokeNumber2Component[componentToConsider].length);
        // console.log(i, randomChar.ids_strokes[i % randomChar.ids_strokes.length], strokeNumber2Component[randomChar.ids_strokes[i]], randomIndex, strokeNumber2Component[randomChar.ids_strokes[i]][randomIndex])
        randomComponents.push(strokeNumber2Component[componentToConsider][randomIndex]);
    }

    return {
        char,
        randomChar,
        randomComponents
    }
}