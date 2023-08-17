function toggleDropdown() {
    var dropdown = document.getElementById("dropdown");
    dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
}

function populateSearchBar(optionId) {
    var selectedOption = document.getElementById(optionId);
    var searchInput = document.getElementById('search');
    var currentSearchValue = searchInput.value;
    
    // Append the selected option value to the search bar
    if (currentSearchValue === '') {
        searchInput.value = selectedOption.value;
    } else {
        searchInput.value = currentSearchValue + ', ' + selectedOption.value;
    }
}

function redirectToProduct(link) {
    window.open(link, '_blank');
}


const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const submitBtn = document.getElementById('submit-btn');
const responseContainer = document.getElementById('response-container');

const model = new GPT4All("orca-mini-3b.ggmlv3.q4_0.bin");

submitBtn.addEventListener('click', async () => {
    const userMessage = userInput.value;
    
    if (userMessage.trim() === '') {
        return;
    }

    addMessage('user', userMessage);
    const response = await generateResponse(userMessage);
    addMessage('bot', response, true);
    
    userInput.value = '';
});

async function generateResponse(prompt) {
    const output = await model.generate(prompt, { max_tokens: 50 });
    return output.choices[0].text;
}

function addMessage(role, content, typingEffect = false) {
    const messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${role}:</strong> `;
    chatHistory.appendChild(messageElement);

    if (typingEffect) {
        const typingEffectInterval = 50; // milliseconds
        let currentIndex = 0;
        const typeMessage = () => {
            if (currentIndex < content.length) {
                messageElement.innerHTML += content.charAt(currentIndex);
                currentIndex++;
                setTimeout(typeMessage, typingEffectInterval);
            }
        };
        typeMessage();
    } else {
        messageElement.innerHTML += content;
    }
}