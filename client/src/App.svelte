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
		<img src="./images/xButton.png" alt="x" class="icon" />
	</button>
	{#if showSidebar}
		<div class="qqContent">
			<p>mfw i am content</p>
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
		width: 20%;
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
		right: 0;
		background-color: red;
	}

	.icon {
		width: 10px;
		height: 10px;
	}

	h1 {
		color: #ff3e00;
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
