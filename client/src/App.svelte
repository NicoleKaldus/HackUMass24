<script>
    import "./styles.css";
    import { onMount, afterUpdate } from "svelte";

    let showSidebar = false;

    let message = ""; // User input
    let messages = []; // All messages in the chat
    let chatBox; // Chatting scroll area
    let input; // User input text area

    /**
     * Gets AI response to user query in form:
     *  { role: "system", content: system_message }
     *
     * If it's the user's first query, initializes with AI route "/init", else continues
     * conversation with "/query".
     * - "/init": takes in query
     * - "/query": takes in query and chat history (user and ai)
     * @param query user text input
     */
    async function getAiResponse(query) {
        const routes = ["/init", "/query"];
        const payload = { input: query };
        // account for user msg being first element
        const isFirstQuery = messages.length < 2;
        if (!isFirstQuery) payload.history = messages;
        const route = isFirstQuery ? routes[0] : routes[1];
        console.log(isFirstQuery, query, route);
        console.log(payload);
        return fetch(route, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        })
            .then(res => {
                console.log("res:", res);
                const resJson = res.json();
                console.log("res json:", resJson);
                return resJson;
            })
            .then(data => {
                // update message history with user then ai response
                messages = data.chat_history;
                // return ai response
                return data.content;
            })
            .catch(e => {
                console.error(e);
                return "Failed to get AI response";
            });
    }

    // Send message when Enter is pressed or button is clicked
    async function sendMessage() {
        // dont send empty input
        if (message.trim() !== "") {
            // Add the user message
            messages = [...messages, { role: "user", content: message }];
            // Simulate AI response after a short delay
            messages = [...messages, await getAiResponse(message)];
            // Clear the input field
            message = "";

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
                <p>FAQ</p>
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
            {#each messages as { content, role }}
                <div class="message {role}">
                    <div class="bubble">{content}</div>
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
</main>

<!-- <style>
	@import './styles.css';
</style> -->
