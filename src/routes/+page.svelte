<script>
	// import { twemoji } from 'svelte-twemoji';
	import { A1F1f01f1f7, A1F1fb1f1f3, A1F1e81f1f3, A1F1ef1f1f5 } from 'svelte-twitter-emoji';

	export let data = {
		randomChar: {
			i: []
			// other properties
		},
		randomComponents: []
		// other properties
	};

	const chinese = true;

	$: console.log(data);

	// let choices = [...data.randomChar.ids, ...data.randomComponents]
	// 	.splice(0, 9)
	// 	.sort(() => Math.random() - 0.5);

	// let choices = [
	// 	...data.randomChar.ids.map((char) => ({ char, ids: true, selected: false })),
	// 	...data.randomComponents.map((char) => ({ char, ids: false, selected: false }))
	// ]
	// 	.splice(0, 9)
	// 	.sort(() => Math.random() - 0.5);
	let choices = [
		...(data.randomChar.i
			? data.randomChar.i.split('').map((char) => ({
					char,
					ids: true,
					selected: false,
					status: 'unselected'
				}))
			: []),
		...(Array.isArray(data.randomComponents) ? data.randomComponents : []).map((char) => ({
			char,
			ids: false,
			selected: false,
			status: 'unselected'
		}))
	]
		.splice(0, 9)
		.sort(() => Math.random() - 0.5);

	// let choiceObjects = [];

	// $: choiceObjects = choices.map((choice) => ({
	// 		char: choice,
	// 		isCorrect: choice === data.randomChar.char,
	// 	}));

	function toggleChoice(index) {
		choices = choices.map((choice, i) => {
			if (i === index) {
				return { ...choice, selected: !choice.selected };
			}
			return choice;
		});
	}

	let showAnswer = false;

	let onyomis = [];
	let kunyomis = [];
	let pinyins = [];
	let korean_rs = [];
	let korean_hs = [];
	let vietnameses = [];

	// Assuming data.randomChar.readingMeaning.groups[0].readings is an array of reading objects
	data.randomChar.readingMeaning?.groups[0].readings.forEach((reading) => {
		switch (reading.type) {
			case 'ja_on':
				onyomis.push(reading.value);
				break;
			case 'ja_kun':
				kunyomis.push(reading.value);
				break;
			case 'pinyin':
				pinyins.push(reading.value);
				break;
			case 'korean_h':
				korean_hs.push(reading.value);
				break;
			case 'korean_r':
				korean_rs.push(reading.value);
				break;
			case 'vietnam':
				vietnameses.push(reading.value);
				break;
			// Add more cases as needed
			default:
				// Handle other types or log them
				break;
		}
	});

	function convertNumericalPinyinToToneMarks(pinyinWithNumber) {
		const toneMarks = {
			a: ['ā', 'á', 'ǎ', 'à'],
			e: ['ē', 'é', 'ě', 'è'],
			i: ['ī', 'í', 'ǐ', 'ì'],
			o: ['ō', 'ó', 'ǒ', 'ò'],
			u: ['ū', 'ú', 'ǔ', 'ù'],
			ü: ['ǖ', 'ǘ', 'ǚ', 'ǜ']
		};

		// Extract the tone number and remove it from the syllable
		const toneNumber = parseInt(pinyinWithNumber.slice(-1));
		const pinyin = pinyinWithNumber.slice(0, -1);

		// Handle the fifth tone (neutral tone) directly
		if (toneNumber === 5) {
			return pinyin; // Return the pinyin without any tone mark
		}

		const adjustedToneNumber = toneNumber - 1; // Adjust for array indexing

		// Find the main vowel to apply the tone mark to
		for (let vowel in toneMarks) {
			if (pinyin.includes(vowel)) {
				// Replace the vowel with its toned counterpart
				return pinyin.replace(vowel, toneMarks[vowel][adjustedToneNumber]);
			}
		}
		return pinyinWithNumber; // Return original if no match (shouldn't happen in proper pinyin)
	}

	// function submitAnswer() {}
	let correctness = 'unsubmitted'; // "correct", "semi-correct", "wrong", "unsubmitted"
	function submitAnswer() {
		let correctChoices = data.randomChar.i;
		let selectedIds = choices.filter((choice) => choice.selected).map((choice) => choice.char);

		// Update choices with correct/incorrect status
		choices = choices.map((choice) => {
			if (correctChoices.includes(choice.char)) {
				// Mark correct choices
				return {
					...choice,
					selected: false,
					status: selectedIds.includes(choice.char) ? 'correct' : 'missed'
				};
			} else {
				// Mark incorrect choices
				return {
					...choice,
					selected: false,
					status: selectedIds.includes(choice.char) ? 'wrong' : 'unselected'
				};
			}
		});

		// Update correctness based on the updated choices
		updateCorrectness();
	}

	function updateCorrectness() {
		const allCorrect = choices.every(
			(choice) => choice.status === 'correct' || choice.status === 'unselected'
		);
		const anyCorrect = choices.some((choice) => choice.status === 'correct');
		const anyWrong = choices.some((choice) => choice.status === 'wrong');

		correctness = allCorrect ? 'correct' : anyCorrect ? 'semi-correct' : 'wrong';
	}
</script>

<svelte:head>
	<title>Hanzi Puzzle</title>
</svelte:head>

<main>
	<div class="game">
		{#if correctness == 'correct'}
			<h1 style="font-weight: 400; font-size: 3rem; margin: 1rem;">{data.randomChar.char}</h1>
		{/if}
		{#if chinese}
			{#each data.randomChar?.w ?? [] as word}
				<p>
					{word.w.replaceAll(data.char, '_')}
					{word.p}
					{word.d}
				</p>
				<!-- {#if word.trad != data.randomChar.char && word.word != data.randomChar.char} -->
				<!-- <p class="topWord">{word.word.replaceAll(data.randomChar.char, '_')} {word.gloss}</p> -->
				<!-- {/if} -->
			{/each}
		{:else}
			<div>
				{#each data.randomChar.readingMeaning?.groups[0].meanings ?? [] as meaning}
					<span class="comma">{meaning.value}</span>
				{/each}
			</div>
			<hr />
			{#if onyomis.length > 0 || kunyomis.length > 0}
				<div>
					<A1F1ef1f1f5 size={16} />
					{#if onyomis.length > 0}
						{#each onyomis as onyomi}<span class="comma-jp">{onyomi}</span
							>{/each}{/if}{#if kunyomis.length > 0}{#each kunyomis as kunyomi}<span
								class="comma-jp">{kunyomi}</span
							>{/each}{/if}
				</div>
			{/if}
			{#if data.randomChar.readingMeaning.nanori.length > 0}
				<div>
					📛
					{#each data.randomChar.readingMeaning.nanori ?? [] as nanori}
						<span class="comma-jp">{nanori}</span>
					{/each}
				</div>
			{/if}
			{#if pinyins.length > 0}
				<div>
					<A1F1e81f1f3 size={16} />
					{#each pinyins as pinyin}<span class="comma"
							>{convertNumericalPinyinToToneMarks(pinyin)}</span
						>{/each}
					<!-- {#each pinyins as pinyin}<span class="comma">{pinyin}</span>{/each} -->
				</div>
			{/if}
			{#if korean_hs.length > 0}
				<div>
					<A1F1f01f1f7 size={16} />
					{#each korean_rs as korean_r, i}
						<span class="comma"><ruby>{korean_hs[i]}<rt>{korean_r}</rt></ruby></span>
					{/each}
				</div>
			{/if}
			{#if vietnameses.length > 0}
				<div>
					<A1F1fb1f1f3 size={16} />
					{#each vietnameses as vietnamese}<span class="comma">{vietnamese}</span>{/each}
				</div>
			{/if}
		{/if}
		<br />
		<div class="choices">
			{#each choices as choice, i}
				<button
					on:click={() => toggleChoice(i)}
					class={choice.selected ? 'selected' : choice.status}
				>
					{choice.char}
				</button>
			{/each}
		</div>

		{#if correctness === 'semi-correct'}
			<p>Some answers are correct, some are not. Retry.</p>
		{:else if correctness === 'wrong'}
			<p>All answers are incorrect. Try again.</p>
		{:else if correctness === 'correct'}
			<p>All answers are correct! Well done.</p>
		{/if}

		<!-- <button on:click={() => submitAnswer()}>Submit Answer</button> -->

		{#if showAnswer}
			<div class="answer">
				<p>{data.char}</p>
			</div>
		{/if}

		{#if choices.some((choice) => choice.selected)}
			<button on:click={() => submitAnswer()}>Submit Answer</button>
		{/if}
		<br />
		<button on:click={() => (showAnswer = !showAnswer)}
			>{showAnswer ? 'Hide' : 'Show'} Answer</button
		>
	</div>
</main>

<style>
	.comma-jp:not(:last-child)::after {
		content: '、';
	}
	.comma:not(:last-child)::after {
		content: ', ';
	}

	main {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100vh;
		width: 100vw;
		text-align: center;
	}

	.choices {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1rem;
		width: 100%;
	}

	.choices button {
		padding: 1rem;
		font-size: 2rem;
		background: grey;
		color: white;
		border: none;
		border-radius: 0.5rem;
		cursor: pointer;
	}

	.gloss {
		font-size: 3rem;
	}

	.topWord {
		font-size: 1.5rem;
	}

	button.selected {
		background: white;
		color: black;
	}

	button.wrong {
		background: red;
	}

	button.semi-correct {
		background: yellow;
	}

	button.correct {
		background: green;
	}
</style>
