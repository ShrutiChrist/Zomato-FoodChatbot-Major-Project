// Get the chatbot container and close button
const chatbotContainer = document.getElementById('chatbotContainer');
const closeButton = document.getElementById('closeButton');

// Add event listener to the close button
closeButton.addEventListener('click', () => {
    chatbotContainer.style.display = 'none'; // Hide the chatbot container
});



// Function to show the chatbot container
function showChatbot() {
    chatbotContainer.style.display = 'block';
}

// Add event listener to the chatbot button to show the chatbot container
chatbotButton.addEventListener('click', showChatbot);
