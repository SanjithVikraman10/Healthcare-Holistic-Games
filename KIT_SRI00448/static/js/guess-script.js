const wordsWithSpecialities = [
  {
    word: "MUMBAI",
    speciality: "🏙️ Financial capital of India and home to Bollywood.",
  },
  {
    word: "DELHI",
    speciality: "🕌 Capital city with a rich historical and cultural heritage.",
  },
  {
    word: "JAIPUR",
    speciality:
      "🎨 Known for its vibrant colors, historical forts, and palaces.",
  },
  {
    word: "TAJMAHAL",
    speciality: "🕌 Iconic white marble mausoleum located in Agra.",
  },
  {
    word: "GANDHI",
    speciality:
      "👴 Father of the Nation and a key figure in India's independence movement.",
  },
  {
    word: "BOLLYWOOD",
    speciality: "🎬 Hindi film industry, one of the largest in the world.",
  },
  {
    word: "YOGA",
    speciality:
      "🧘 Ancient practice for physical, mental, and spiritual well-being.",
  },
  {
    word: "HIMALAYAS",
    speciality:
      "🏔️ World's highest mountain range, known for breathtaking landscapes.",
  },
  {
    word: "GANGES",
    speciality: "🌊 Sacred river in India, considered holy by Hindus.",
  },
  {
    word: "KERALA",
    speciality:
      "🌴 Beautiful state known for its backwaters, beaches, and Ayurvedic practices.",
  },
  {
    word: "RANGOLI",
    speciality:
      "🎨 Colorful art form created during festivals and special occasions.",
  },
  {
    word: "SAMOSA",
    speciality: "🥟 Popular Indian snack with a savory filling.",
  },
  {
    word: "KATHAK",
    speciality:
      "💃 Classical Indian dance form known for its intricate footwork.",
  },
  {
    word: "DIWALI",
    speciality:
      "✨ Festival of lights, celebrated with lamps, fireworks, and sweets.",
  },
  {
    word: "KOLKATA",
    speciality:
      "📚 City known for its literary culture, historical landmarks, and Durga Puja festival.",
  },
  {
    word: "MYSOREPALACE",
    speciality:
      "🏰 Historical palace in Mysore, Karnataka, known for its architecture.",
  },
  {
    word: "KASHMIR",
    speciality:
      "🏞️ Region known for its picturesque landscapes, lakes, and traditional handicrafts.",
  },
  {
    word: "VINDHYACHAL",
    speciality:
      "⛰️ Sacred hill range in central India, known for religious significance.",
  },
  {
    word: "MANGO",
    speciality: "🥭 King of fruits, enjoyed for its sweet and juicy taste.",
  },
  {
    word: "CHAAT",
    speciality:
      "🍲 Popular street food in India, known for its tangy and spicy flavors.",
  },
  {
    word: "AYURVEDA",
    speciality:
      "🌿 Traditional system of medicine with roots in ancient India.",
  },
  {
    word: "BHANGRA",
    speciality: "💃 Energetic and vibrant traditional Punjabi dance.",
  },
  {
    word: "JODHPUR",
    speciality: "🏰 Famous for its blue-painted buildings and Mehrangarh Fort.",
  },
  {
    word: "LADAKH",
    speciality:
      "🏔️ High-altitude region known for its stunning landscapes and monasteries.",
  },
  {
    word: "BHARATNATYAM",
    speciality: "💃 Classical Indian dance form originating from Tamil Nadu.",
  },
  {
    word: "GOA",
    speciality:
      "🏖️ Popular tourist destination with beautiful beaches and vibrant nightlife.",
  },
  {
    word: "COORG",
    speciality:
      "🏞️ Picturesque hill station known for coffee plantations and lush greenery.",
  },
  {
    word: "RISHIKESH",
    speciality:
      "🧘 Yoga capital of the world, located on the banks of the Ganges River.",
  },
  {
    word: "TAMILNADU",
    speciality:
      "🏰 State with rich cultural heritage, known for temples and classical music.",
  },
  {
    word: "ANDHRA PRADESH",
    speciality:
      "🏛️ Known for its rich cultural heritage and historical monuments.",
  },
  {
    word: "ARUNACHAL PRADESH",
    speciality: "🌄 Land of the rising sun, known for its scenic beauty.",
  },
  {
    word: "ASSAM",
    speciality: "🍵 Famous for tea plantations and the one-horned rhinoceros.",
  },
  {
    word: "BIHAR",
    speciality: "🌅 Land of enlightenment, home to Bodh Gaya and Nalanda.",
  },
  {
    word: "CHHATTISGARH",
    speciality: "🌳 Abundant in natural resources and tribal culture.",
  },
  {
    word: "GOA",
    speciality:
      "🏖️ Popular tourist destination with beautiful beaches and vibrant nightlife.",
  },
  {
    word: "GUJARAT",
    speciality: "🏛️ Known for its rich industrial and cultural heritage.",
  },
  {
    word: "HARYANA",
    speciality: "🌾 Land of rich agriculture and historical significance.",
  },
  {
    word: "HIMACHAL PRADESH",
    speciality: "🏔️ Abode of the Himalayas, known for scenic landscapes.",
  },
  {
    word: "JHARKHAND",
    speciality: "⛏️ Rich in minerals and known for its tribal culture.",
  },
  {
    word: "KARNATAKA",
    speciality: "🏞️ Land of diverse landscapes, IT hub, and historical sites.",
  },
  {
    word: "KERALA",
    speciality:
      "🌴 Beautiful state known for its backwaters, beaches, and Ayurvedic practices.",
  },
  {
    word: "MADHYA PRADESH",
    speciality:
      "🏰 Heart of India, known for historical landmarks and wildlife.",
  },
  {
    word: "MAHARASHTRA",
    speciality: "💼 Financial capital, home to Bollywood, and diverse culture.",
  },
  {
    word: "MANIPUR",
    speciality: "💃 Known for its classical dance form and scenic beauty.",
  },
  {
    word: "MEGHALAYA",
    speciality: "☁️ Abode of clouds, known for waterfalls and natural beauty.",
  },
  {
    word: "MIZORAM",
    speciality: "🎉 Land of the Mizos, known for its vibrant festivals.",
  },
  {
    word: "NAGALAND",
    speciality: "👥 Known for its tribal culture and Hornbill Festival.",
  },
  {
    word: "ODISHA",
    speciality: "🕍 Land of temples, known for its ancient architecture.",
  },
  {
    word: "PUNJAB",
    speciality: "🌊 Land of five rivers, known for Bhangra and Sikh culture.",
  },
  {
    word: "RAJASTHAN",
    speciality: "🏰 Land of kings, known for its deserts, forts, and palaces.",
  },
  {
    word: "SIKKIM",
    speciality: "🌳 Known for its biodiversity and monasteries.",
  },
  {
    word: "TELANGANA",
    speciality:
      "💻 Newest state, known for its IT industry and historical sites.",
  },
  {
    word: "TRIPURA",
    speciality: "🎍 Known for its bamboo handicrafts and diverse culture.",
  },
  {
    word: "UTTAR PRADESH",
    speciality:
      "🌊 Land of the Ganges, known for Taj Mahal and religious sites.",
  },
  {
    word: "UTTARAKHAND",
    speciality:
      "⛰️ Abode of the gods, known for pilgrimage sites and trekking.",
  },
  {
    word: "WEST BENGAL",
    speciality: "🎭 Cultural capital, known for Durga Puja and literature.",
  },
];

let selectedWord = "";
let guessedWord = [];
let guessedLetters = [];
let attemptsLeft = 6;

function setupGame() {
  selectedWord = selectRandomWord();
  guessedWord = Array(selectedWord.length).fill("_");
  guessedLetters = [];
  attemptsLeft = 6;
  updateDisplay();
}

function selectRandomWord() {
  const randomIndex = Math.floor(Math.random() * wordsWithSpecialities.length);
  return wordsWithSpecialities[randomIndex].word;
}

function getSpeciality() {
  const wordObject = wordsWithSpecialities.find(
    (obj) => obj.word === selectedWord
  );
  return wordObject
    ? wordObject.speciality
    : "No speciality information available.";
}

function updateDisplay() {
  const wordDiv = document.getElementById("word");
  const lettersDiv = document.getElementById("letters");
  const messageDiv = document.getElementById("message");

  wordDiv.textContent = guessedWord.join(" ");
  lettersDiv.innerHTML = "";

  for (let i = 65; i <= 90; i++) {
    const letter = String.fromCharCode(i);
    const letterBtn = document.createElement("button");
    letterBtn.textContent = letter;
    letterBtn.onclick = () => guessLetter(letter);
    lettersDiv.appendChild(letterBtn);
  }

  messageDiv.textContent = `Attempts left: ${attemptsLeft}`;
}

function guessLetter(letter) {
  if (guessedLetters.includes(letter)) {
    return; // Letter already guessed
  }

  guessedLetters.push(letter);

  if (selectedWord.includes(letter)) {
    for (let i = 0; i < selectedWord.length; i++) {
      if (selectedWord[i] === letter) {
        guessedWord[i] = letter;
      }
    }
  } else {
    attemptsLeft -= 1;
  }

  updateDisplay();

  if (guessedWord.join("") === selectedWord) {
    showSpeciality();
  } else if (attemptsLeft === 0) {
    showMessage(
      `Sorry! The correct word was "${selectedWord}" - ${getSpeciality()}`
    );
  }
}

function showSpeciality() {
  const speciality = getSpeciality();
  showMessage(
    `Congratulations! You guessed the word!
    ${speciality}`
  );
}

function showMessage(message) {
  const messageDiv = document.getElementById("message");
  messageDiv.textContent = message;
}

function resetGame() {
  setupGame();
}

// Initial setup
setupGame();
