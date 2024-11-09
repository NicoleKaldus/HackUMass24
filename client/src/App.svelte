<script>
	let showSidebar = false;
	export let name;
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>See <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">next steps</a> to view our future plans.</p>
</main>

<div class="flex-container">
	<button on:click={() => (showSidebar = !showSidebar)}>
		{#if showSidebar}
			<img src="./images/chevronLeft.png" alt="x" class="icon" />
		{:else}
			<img src="./images/chevronRight.png" alt="x" class="icon" />
		{/if}
	</button>
	{#if showSidebar}
		<div class="qqContent">
			<p>mfw i am content0</p>
			<p>mfw i am content1</p>
			<p>mfw i am content2</p>
			<p>mfw i am content3</p>
			<p>mfw i am content4</p>
			<p>mfw i am content5</p>
			<p>mfw i am content6</p>
			<p>mfw i am content7</p>
			<p>mfw i am content8</p>
		</div>
	{/if}
</div>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	.flex-container {
		position: absolute;
		top: 15%;
		background: greenyellow;
		color: white;
		width: fit-content;
		height: fit-content;
		padding: 3px;
	}

	.qqContent {
		position: relative;
		left: 0;
		background: blue;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        margin: auto;
        height: 100%;
		column-gap: 1px;
    }

	p {
		margin: 0.5em;
	}

	button {
		position: relative;
		float: right;
		background-color: green;
	}

	.icon {
		width: 1em;
		height: 1em;
	}

	h1 {
		color: blue;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
