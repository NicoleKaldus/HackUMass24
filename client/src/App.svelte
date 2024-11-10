<script>
    import './styles.css';
    import { onMount, afterUpdate } from 'svelte';

    let showSidebar = true;
    let showInfo = true;
    let isSam = true;
    let message = ""; // User input
    let placeholder = "I'm Sam! I can tell you anything from official sources!";
    let messages = []; // All messages in the chat
    let chatBox; // Chatting scroll area
    let input; // User input text area

    messages = [...messages, { text: placeholder, sender: "ai" }];

    // FAQ array with key-value pairs
    const faqItems = [
        { title: "Majors & Minors", content: "What are the requirements for a BS in Computer Science?" },
        { title: "Gen-Ed Requirements", content: "What are the gen-ed requirements to graduate?" },
        { title: "Residential Areas", content: "What are the pros and cons of living at Northeast?" },
        { title: "Residential Halls", content: "What is the atmosphere like at Mary Lyon Hall?" },
        { title: "Dining Halls", content: "At what times do the dining halls close?" },
        { title: "Transportation", content: "How can I get to CVS without a car?" },
        { title: "Clubs", content: "How can I join the cybersecurity club?" },
        { title: "Activities", content: "What can I do for fun around Amherst?" }
    ];

    // Simulated AI response function
    function getAiResponse(userMessage) {
        let response = `AI response to: ${userMessage}`;
        if(!isSam){
            if(Math.floor(Math.random() * 10) < 4){
                response += " Honk!";
            }
        }
        return response;
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
        input.focus();
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

    // Toggle the title between "Sam.ai" and "Goose.ai"
    function toggleTitle() {
        messages = [];
        if(isSam){
            this.style.color = "gray";
            placeholder = "Honk! I'm goose! I'm up to date with the community gossip!";
        }
        else{
            this.style.color = "rgb(136, 28, 28)";
            placeholder = "I'm Sam! I can tell you anything from official sources!";
        }
        isSam = !isSam;
        messages = [...messages, { text: placeholder, sender: "ai" }];
    }
</script>

<main>
    <button class="titleBtn" on:click={toggleTitle}>{isSam ? "Sam.ai" : "Goose.ai"}</button>

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
                <div class="faqHeader">
                    <p>FAQ</p>
                </div>
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
        <div class="chat-box" bind:this={chatBox}>
            {#each messages as { text, sender }}
                <div class="message {sender}">
                    <div class="bubble" 
                         style="background-color: {sender === 'ai' ? (isSam ? 'rgba(136, 28, 28, 0.747)' : 'rgb(211, 211, 211)') : ''}; 
                                color: {sender === 'ai' ? (isSam ? 'rgb(211, 211, 211)' : 'black') : ''};">
                         {text}
                    </div> 
                </div>
            {/each}
        </div>

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
        <div class = "account-container">
            <button class="loginBtn">Log in</button>
            <button class="signupBtn">Sign up</button>
        </div>
        {#if showInfo}
            <div class="info bottom">
                <div>
                    <h3>Sam</h3>
                    <p class="infoinfo">will tell you what's on official sources.</p>
                </div>
                <div>
                    <h3>Goose</h3>
                    <p class="infoinfo">will tell you what the community says.</p>
                </div>
                <div>
                    <p class="infoinfo">Click the title to switch your conversation partner!</p>
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
