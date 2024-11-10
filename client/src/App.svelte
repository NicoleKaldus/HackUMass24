<script>
    import "./styles.css";
    import { onMount, afterUpdate, tick } from "svelte";
    import { marked } from "marked";

    let chatBox; // Chatting scroll area
    let input; // User input text area
    let showSidebar = true;
    let showInfo = true;
    let isSam = true;
    let message = ""; // User input
    const sam_prompt = {
        role: "system",
        content:
            "You are Sam the Minuteman, the official mascot of the University of Massachusetts Amherst, also known as UMass Amherst. You are a helpful assistant for students and try to be as unbiased as possible when answering students.",
    };
    const goose_prompt = {
        role: "system",
        content:
            "You are a goose with a strong, mischievous personality at the University of Massachusetts Amherst, also known as UMass Amherst. You are an assistant for students and you aren't afraid to show your bias towards water, fresh greens, and adventure. You represent the voice of the general student community, so you tend to have subjective and sometimes strongly opinionated answers, with a little sass",
    };
    let placeholder = "I'm Sam! I can tell you anything about UMass Amherst from official sources!";
    // All messages in the chat, init with prompt and welcome message
    let messages = [sam_prompt, { role: "assistant", content: placeholder }];
    let loading = false;

    // FAQ array with key-value pairs
    const faqItems = [
        {
            title: "Majors & Minors",
            content: "What are the requirements for a BS in Computer Science?",
        },
        { title: "Gen-Ed Requirements", content: "What are the gen-ed requirements to graduate?" },
        {
            title: "Residential Areas",
            content: "What are the pros and cons of living at Northeast?",
        },
        { title: "Residential Halls", content: "What is the atmosphere like at Mary Lyon Hall?" },
        { title: "Dining Halls", content: "At what times do the dining halls close?" },
        { title: "Transportation", content: "How can I get to CVS without a car?" },
        { title: "Clubs", content: "How can I join the cybersecurity club?" },
        { title: "Activities", content: "What can I do for fun around Amherst?" },
    ];

    /**
     * Gets AI response to user query in form:
     *  { role: "assistant", content: system_message }
     *
     * If it's the user's first query, initializes with AI route "/init", else continues
     * conversation with "/query".
     * - "/init": takes in query
     * - "/query": takes in query and chat history (user and ai)
     * @param query user text input
     * @returns data.content
     */
    async function getAiResponse(query) {
        const routes = ["/init", "/query"];
        const payload = { input: query, isSam: isSam };
        // account for prompt, welcome msg, and user msg
        const isFirstQuery = messages.length < 4;
        const route = isFirstQuery ? routes[0] : routes[1];
        if (isFirstQuery) {
            // initial ai prompt
            payload.prompt = isSam ? sam_prompt.content : goose_prompt.content;
        } else {
            // add chat history to following queries
            payload.history = messages;
        }

        return fetch(route, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        })
            .then(res => {
                const resJson = res.json();
                return resJson;
            })
            .then(data => {
                // return ai response
                console.log(2, messages);
                let msg = data.content;
                if (!isSam) {
                    if (Math.floor(Math.random() * 10) < 4) {
                        msg += " Honk!";
                    }
                }
                return msg;
            })
            .catch(e => {
                console.error(e);
                return "Failed to get AI response";
            });
    }

    // Send message when Enter is pressed or button is clicked
    async function sendMessage() {
        loading = true;
        // dont send empty input
        if (message.trim() !== "") {
            // Add the user message
            messages = [...messages, { role: "user", content: message }];
            // Simulate AI response after a short delay
            console.log(3, messages);
            const response = await getAiResponse(message);
            messages = [
                ...messages,
                { role: "assistant", content: marked(response.replace(/\n/g, "<br>")) },
            ];
            // messages = new_history;
            // messages.push(response);
            console.log(4, messages);
            // Clear the input field
            message = "";
        }
        loading = false;
        // wait till input is reenabled to refocus
        tick().then(() => input.focus());
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
        if (isSam) {
            this.style.color = "gray";
            placeholder =
                "Honk! I'm goose! I'm up to date with the community gossip about UMass Amherst!";
        } else {
            this.style.color = "rgb(136, 28, 28)";
            placeholder =
                "I'm Sam! I can tell you anything about UMass Amherst from official sources!";
        }
        isSam = !isSam;
        messages = [sam_prompt, { role: "assistant", content: placeholder }];
        messages[0] = isSam ? sam_prompt : goose_prompt;
        console.log(messages);
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
                    <button class="faqBtn" on:click={() => (message = content)}>
                        {title}
                    </button>
                {/each}
            </div>
        {/if}
    </div>

    <div class="chat-container">
        <div class="chat-box" bind:this={chatBox}>
            {#each messages as { content, role }}
                {#if role !== "system"}
                    <div class="message {role}">
                        <div
                            class="bubble"
                            style="background-color: {role === 'assistant'
                                ? isSam
                                    ? 'rgba(136, 28, 28, 0.747)'
                                    : 'rgb(211, 211, 211)'
                                : ''};
                                color: {role === 'assistant'
                                ? isSam
                                    ? 'rgb(211, 211, 211)'
                                    : 'black'
                                : ''};"
                        >
                            {@html content}
                        </div>
                    </div>
                {/if}
            {/each}

            {#if loading}
                <div class="message assistant">
                    <div class="bubble thinking">
                        <span>Thinking...</span>
                    </div>
                </div>
            {/if}
        </div>

        <div class="input-container">
            <input
                bind:this={input}
                type="text"
                bind:value={message}
                placeholder="Type a message..."
                on:keydown={handleKeydown}
                disabled={loading}
            />
            <button class="inputBtn" on:click={sendMessage} disabled={loading}>Send</button>
        </div>
    </div>

    <div class="desc-container">
        <div class="account-container">
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
