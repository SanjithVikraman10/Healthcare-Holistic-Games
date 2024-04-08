const images = [
  "🍎", // Apple
  "🍐", // Pear
  "🥑", // Avocado
  "🥦", // Broccoli
  "🍓", // Strawberry
  "🍇", // Grapes
  "🍌", // Banana
  "🍆", // Eggplant
  "🥕", // Carrot
  "🌽", // Corn
  "🍍", // Pineapple
  "🍊", // Orange
  "🍉", // Watermelon
  "🍈", // Cantaloupe
  "🍒", // Cherry
  "🍑", // Peach
  "🍅", // Tomato
  "🍋", // Lemon
  "🍏", // Green Apple
  "🥭", // Mango
];

// Map each image to its one-line benefit description
const imageDescriptions = {
  "🍎": ": Apple is rich in fiber and antioxidants. Supports heart health.",
  "🍐": ": Pear is high in vitamins and minerals. Aids digestion.",
  "🥑": ": Avacado is packed with healthy fats and nutrients. Good for skin and heart.",
  "🥦": ": Broccoli is high in fiber, vitamins, and minerals. Supports immune system.",
  "🍓": ": Strawberry is full of antioxidants. Promotes skin health.",
  "🍇": ": Grapes is rich in vitamins and antioxidants. Supports heart health.",
  "🍌": ": Banana is a great source of energy. Supports digestion.",
  "🍆": ": Eggplant is low in calories. Contains vitamins and minerals.",
  "🥕": ": Carrot is rich in beta-carotene. Supports eye health.",
  "🌽": ": Corn is a good source of fiber and antioxidants.",
  "🍍": ": Pineapple is high in vitamin C. Supports immune system.",
  "🍊": ": Orange is rich in vitamin C. Promotes skin health.",
  "🍉": ": Watermelon is hydrating and refreshing. Contains vitamins A and C.",
  "🍈": ": Cantaloupe is low in calories and high in vitamins. Supports hydration.",
  "🍒": ": Cherry is rich in antioxidants. Supports heart health.",
  "🍑": ": Peach is high in fiber and vitamins. Supports skin health.",
  "🍅": ": Tomato is packed with vitamins and antioxidants. Good for heart health.",
  "🍋": ": Lemon is high in vitamin C. Refreshing and tangy.",
  "🍏": ": Green Apple is rich in fiber and antioxidants. Supports digestive health.",
  "🥭": ": Mango is sweet and juicy. High in vitamins A and C.",
};

let cards = [];
let flippedCards = [];
let matchedPairs = 0;
let moves = 0;
let score = 0;
let startTime;
let timerInterval;
let isPaused = false;
let pausedTime = 0;
let elapsedPauseTime = 0; // Store elapsed time during pause

function setupGame() {
  const doubledImages = [...images, ...images];
  shuffleArray(doubledImages);

  const gameContainer = document.getElementById("game-container");

  doubledImages.forEach((image, index) => {
    const card = document.createElement("div");
    card.classList.add("card");
    card.dataset.index = index;
    card.innerText = "?";
    card.addEventListener("click", flipCard);
    gameContainer.appendChild(card);
    cards.push({ element: card, image, flipped: false });
  });
  startTimer();
}

function flipCard() {
  const clickedCard = this;
  const index = clickedCard.dataset.index;

  // Check if the timer is not paused and no message is being displayed
  if (!isPaused && document.getElementById("message").innerText === "") {
    if (!cards[index].flipped && flippedCards.length < 2) {
      clickedCard.innerText = cards[index].image;
      cards[index].flipped = true;
      flippedCards.push(cards[index]);

      if (flippedCards.length === 2) {
        moves += 1;
        updateScore();
        setTimeout(checkMatch, 1000);
      }
    }
  }
}

function checkMatch() {
  const [card1, card2] = flippedCards;

  if (card1.image === card2.image) {
    matchedPairs += 1;
    score += 1;
    updateScore();

    if (matchedPairs === images.length) {
      stopTimer();
      document.getElementById("message").innerText =
        "Congratulations! You've matched all pairs.";
      setTimeout(() => {
        document.getElementById("message").innerText = "";
        resetGame();
      }, 3000); // Clear the message after 3 seconds
    } else {
      const description = imageDescriptions[card1.image];
      pauseTimer(); // Pause the timer
      document.getElementById(
        "message"
      ).innerText = `You've matched a pair!\n${card1.image} ${description}`;
      setTimeout(() => {
        document.getElementById("message").innerText = "";
        resumeTimer(); // Resume the timer
        updateTimer();
      }, 10000); // Clear the message after 3 seconds (adjust the duration as needed)
    }
  } else {
    card1.element.innerText = "?";
    card2.element.innerText = "?";
    card1.flipped = false;
    card2.flipped = false;
  }

  flippedCards = [];
}

function updateScore() {
  const scoreElement = document.getElementById("score");
  scoreElement.innerText = `Moves: ${moves} | Score: ${score}`;
}

function startTimer() {
  startTime = Date.now() - elapsedPauseTime;
  timerInterval = setInterval(updateTimer, 1000);
}

function updateTimer() {
  const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
  const remainingSeconds = Math.max(0, 300 - elapsedSeconds);

  document.getElementById("timer").innerText = `Time: ${formatTime(
    remainingSeconds
  )}`;

  if (remainingSeconds === 0) {
    stopTimer();
    alert(`Time's up! Your final score is ${score} in ${moves} moves.`);
    resetGame();
  }
}
function stopTimer() {
  clearInterval(timerInterval);
}

function resetGame() {
  const gameContainer = document.getElementById("game-container");
  gameContainer.innerHTML = "";
  cards = [];
  matchedPairs = 0;
  flippedCards = [];
  moves = 0;
  stopTimer();
  updateScore();
  setupGame();
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${padZero(minutes)}:${padZero(remainingSeconds)}`;
}

function padZero(number) {
  return number < 10 ? `0${number}` : number;
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function pauseTimer() {
  clearInterval(timerInterval);
  elapsedPauseTime = Date.now() - startTime;
}

function resumeTimer() {
  startTimer();
}

// Initialize the game when the page loads
document.addEventListener("DOMContentLoaded", () => {
  setupGame();
  updateScore();
});
