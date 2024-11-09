<script>
    import './styles.css';
	import { onMount, afterUpdate } from 'svelte';

    let showSidebar = false;

    let message = ""; // User input
    let messages = []; // All messages in the chat
    let chatBox; // Chatting scroll area

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
                <button class="faqBtn" id="b0" on:click={() => (message = "sample faq content 0")}>
                    mfw i am content0
                </button>
                <button class="faqBtn" id="b1" on:click={() => (message = "sample faq content 1")}>
                    mfw i am content1
                </button>
                <button class="faqBtn" id="b2" on:click={() => (message = "sample faq content 2")}>
                    mfw i am content2
                </button>
                <button class="faqBtn" id="b3" on:click={() => (message = "sample faq content 3")}>
                    mfw i am content3
                </button>
                <button class="faqBtn" id="b4" on:click={() => (message = "sample faq content 4")}>
                    mfw i am content4
                </button>
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
                type="text"
                bind:value={message}
                placeholder="Type a message..."
                on:keydown={handleKeydown}
            />
            <button class="inputBtn" on:click={sendMessage}>Send</button>
        </div>
    </div>
</main>

<!-- <style>
	@import './styles.css';
</style> -->
