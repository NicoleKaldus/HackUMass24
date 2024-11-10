<script>
    import './styles.css';
    import { onMount, afterUpdate } from 'svelte';

    let showSidebar = true;
	let showInfo = true;
    let message = ""; // User input
    let messages = []; // All messages in the chat
    let chatBox; // Chatting scroll area
    let input; // User input text area

    // FAQ array with key-value pairs
    const faqItems = [
        { title: "Majors & Minors", content: "Majors & Minors content" },
        { title: "Gen-Ed Requirements", content: "Gen-Ed Requirements content" },
        { title: "Living", content: "Living content" },
        { title: "Central", content: "Central content" },
        { title: "Honors College (CHCRC)", content: "Honors College content" },
        { title: "Northeast (NE)", content: "Northeast content" },
        { title: "Orchard Hill (OHill)", content: "Orchard Hill content" },
        { title: "Southwest (SW)", content: "Southwest content" },
        { title: "Sylvan", content: "Sylvan content" },
        { title: "North Apartments", content: "North Apartments content" }
    ];

    // Simulated AI response function
    function getAiResponse(userMessage) {
        return `AI response to: ${userMessage}`;
    }

    // Send message when Enter is pressed or button is clicked
    function sendMessage() {
        if (message.trim() !== "") {
            // Add the user message
            messages = [...messages, { text: message, sender: "user" }];
            // Clear the input field
            message = "";

            // Simulate AI response after a short delay
            messages = [
                ...messages,
                {
                    text: getAiResponse(messages[messages.length - 1].text),
                    sender: "ai",
                },
            ];

            input.focus();
        }
    }

    // This function ensures that the chat container is always scrolled to the bottom
    function updateScrollArea() {
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Use the afterUpdate lifecycle hook to ensure the scroll happens after message is added
    afterUpdate(() => {
        updateScrollArea();
    });

    // Handle Enter key to send message
    function handleKeydown(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }

	function toggleTitle() {
		if (this.innerText === "Sam.ai"){
			this.innerText = "Goose.ai";
		}
		else {
			this.innerText = "Sam.ai"
		}
	}
</script>

<main>
    <div class="faqContainer">
        <button class="menuBtn" on:click={() => (showSidebar = !showSidebar)}>
            {#if showSidebar}
                <img src="./images/chevronLeft.png" alt="x" class="icon" />
            {:else}
                <img src="./images/chevronRight.png" alt="x" class="icon" />
            {/if}
        </button>

        {#if showSidebar}
            <div class="faqContent">
                <div class = "faqHeader">
					<p>FAQ</p>
				</div>
                <!-- Loop through faqItems and create a button for each -->
                {#each faqItems as { title, content }}
                    <button
                        class="faqBtn"
                        on:click={() => (message = content)}
                    >
                        {title}
                    </button>
                {/each}
            </div>
        {/if}
    </div>

    <div class="chat-container">
        <!-- Chat Messages -->
        <div class="chat-box" bind:this={chatBox}>
            {#each messages as { text, sender }}
                <div class="message {sender}">
                    <div class="bubble">{text}</div>
                </div>
            {/each}
        </div>

        <!-- Input Box and Send Button -->
        <div class="input-container">
            <input
                bind:this={input}
                type="text"
                bind:value={message}
                placeholder="Type a message..."
                on:keydown={handleKeydown}
            />
            <button class="inputBtn" on:click={sendMessage}>Send</button>
        </div>
    </div>

	<div class="desc-container">
		<button class="titleBtn" on:click={toggleTitle}>Sam.ai</button>
		{#if showInfo}
			<div class="info bottom">
				<div>
					<h3>Sam</h3>
					<p class = "infoinfo">will tell you what's on official sources.</p>
				</div>
				<div>
					<h3>Goose</h3>
					<p class = "infoinfo">will tell you what the community says.</p>
				</div>
			</div>
		{/if}
		<button class="infoBtn" on:click={() => (showInfo = !showInfo)}>
			<img src="./images/info.png" alt="info" class="icon" />
        </button>
	</div>
</main>


<!-- <style>
	@import './styles.css';
</style> -->
