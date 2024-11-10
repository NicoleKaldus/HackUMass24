<script>
    export let onLogin;
    let username = "";
    let password = "";

    function handleLogin(event) {
        event.preventDefault();
        // Call the login function passed as a prop (simulate login)
        onLogin(username, password);
    }
</script>

<main class="login-container">
    <h1>Log In</h1>
    <form on:submit={handleLogin}>
        <input
            type="text"
            placeholder="Username"
            bind:value={username}
            required
            class="login-input"
        />
        <input
            type="password"
            placeholder="Password"
            bind:value={password}
            required
            class="login-input"
        />
        <button type="submit" class="login-button">Log In</button>
    </form>
</main>

<style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background-color: #f9f9f9;
    }

    h1 {
        color: rgb(136,28,28);
    }

    form {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .login-input {
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
        width: 250px;
        font-size: 16px;
    }

    .login-button {
        padding: 10px;
        border-radius: 8px;
        border: none;
        background-color: rgb(136,28,28);
        color: white;
        font-size: 16px;
        cursor: pointer;
    }

    .login-button:hover {
        background-color: rgb(100, 20, 20);
    }
</style>
