<script>
    let showSidebar = false;
    export let name;

    let message = ""; // User input
    let messages = []; // All messages in the chat

    // Simulated AI response function
    function getAiResponse(userMessage) {
        return `AI response to: ${userMessage}`;
    }

    // Send message when Enter is pressed or button is clicked
    function sendMessage() {
        if (message.trim() !== "") {
            // Add the user message
            messages.push({ text: message, sender: "user" });
            // Clear the input field
            message = "";

            // Simulate AI response after a short delay
            setTimeout(() => {
                messages.push({
                    text: getAiResponse(messages[messages.length - 1].text),
                    sender: "ai",
                });
            }, 1000); // AI responds after 1 second
        }
    }

    // Handle Enter key to send message
    function handleKeydown(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }
</script>

<main>
    <h1>Hello {name}!</h1>
    <p>
        See <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">next steps</a> to view our future plans.
    </p>

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

    <div class="chat-container">
        <!-- Chat Messages -->
        <div class="chat-box">
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
            <button on:click={sendMessage}>Send</button>
        </div>
    </div>
</main>

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

    /* Chat Container */
    .chat-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        height: 100vh;
        max-width: 60vw;
        margin: 0 auto;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
    }

    /* Chat Messages Box */
    .chat-box {
        display: flex;
        flex-direction: column;
        gap: 10px;
        overflow-y: auto;
        max-height: calc(100vh - 160px); /* Adjust height to leave space for input */
        padding: 10px;
    }

    .message {
        display: flex;
        align-items: flex-end;
        justify-content: flex-start;
        max-width: 70%;
    }

    .message.ai {
        justify-content: flex-end;
    }

    /* Message Bubble Styles */
    .bubble {
        max-width: 80%;
        padding: 10px;
        border-radius: 10px;
        background-color: #f1f1f1;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    }

    .message.user .bubble {
        background-color: #007bff;
        color: white;
        align-self: flex-start;
    }

    .message.ai .bubble {
        background-color: #f8f8f8;
        color: #333;
        align-self: flex-end;
    }

    /* Input Box and Send Button */
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }

    input {
        width: 100%;
        padding: 10px;
        border-radius: 25px;
        border: 1px solid #ddd;
        font-size: 14px;
    }

    button {
        padding: 10px 20px;
        border-radius: 25px;
        border: none;
        background-color: #007bff;
        color: white;
        cursor: pointer;
    }

    button:hover {
        background-color: #0056b3;
    }
</style>
