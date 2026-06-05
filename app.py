const jokeElement = document.getElementById('joke');
const jokeBtn = document.getElementById('jokeBtn');

jokeBtn.addEventListener('click', generateJoke);

// Call the function once when the page loads
generateJoke();

async function generateJoke() {
    // Set loading text while we wait for the API
    jokeElement.innerHTML = "Thinking of a good one...";

    const config = {
        headers: {
            Accept: 'application/json',
        },
    };

    try {
        const response = await fetch('https://icanhazdadjoke.com/', config);
        const data = await response.json();
        
        // Put the joke into the HTML
        jokeElement.innerHTML = data.joke;
    } catch (error) {
        jokeElement.innerHTML = "Oops! Something went wrong. Try again.";
    }
}
