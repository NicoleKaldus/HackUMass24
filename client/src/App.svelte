<script>
	let showSidebar = false;
	export let name;
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>See <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">next steps</a> to view our future plans.</p>
</main>

<button on:click={() => (showSidebar = !showSidebar)}><img src="./images/xButton.png" alt = "x"></button>
<div class="flex-container">
	{#if showSidebar}
	<div class="qqContent">
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

	.qqContent {
		position: absolute;
		left: 0;
		width: 30%;
		background: blue;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        margin: auto;
        height: 100%;
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