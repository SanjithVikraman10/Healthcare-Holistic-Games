document.addEventListener('DOMContentLoaded', function() {
    const startContainer = document.getElementById('start-container');
    const mainContainer = document.getElementById('main-container');
    const startBtn = document.getElementById('start-btn');
    const leftSide = document.querySelector('.left-side');
    const draggableItems = document.querySelectorAll('.draggable-item');
    let isGameStarted = false;
    let score = 0;
    let timer;
    const gameDuration = 30; 
    const timeLeftElement = document.getElementById('time-left');
    const scoreElement = document.getElementById('current-score');

    function updateTimerDisplay(timeLeft) {
        timeLeftElement.textContent = timeLeft;
    }

    function updateScoreDisplay(currentScore) {
        scoreElement.textContent = currentScore;
    }

    startBtn.addEventListener('click', function() {
        startContainer.style.display = 'none';
        mainContainer.style.display = 'block';
        leftSide.style.display = 'block';
        isGameStarted = true;
        showDraggableItems();
        score = 0; // Reset score on game start
        startTimer();
        document.getElementById('timer').style.display = 'block';
        document.getElementById('score').style.display = 'block';
    });

    function startTimer() {
        let timeLeft = gameDuration;
        timer = setInterval(function() {
            timeLeft--;
            updateTimerDisplay(timeLeft); // Update timer display

            if (timeLeft === 0) {
                clearInterval(timer);
                endGame();
            }
        }, 1000);
    }
    


    function endGame() {
        
        console.log('Game Over');
        const modal = document.getElementById('myModal');
    const finalScore = document.getElementById('final-score');
    const exitBtn = document.getElementById('exitBtn');

    // Set the final score
    finalScore.textContent = score;

    // Display the modal
    modal.style.display = 'block';

    // Exit button functionality
    exitBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        window.location.href = "child_index.html"; 
    });

        
    }


    function showDraggableItems() {
        draggableItems.forEach(function(item) {
            item.style.display = 'block';
            makeDraggable(item);
        });
    }

    function makeDraggable(item) {
        if (isGameStarted) {
            item.draggable = true;
            item.addEventListener('dragstart', function(event) {
                event.dataTransfer.setData('text/plain', item.dataset.itemType);
            });
        }
    }
    
    const dropAreas = document.querySelectorAll('.droparea');

    dropAreas.forEach(function(dropArea) {
        dropArea.addEventListener('dragover', function(event) {
            event.preventDefault();
        });

        dropArea.addEventListener('drop', function(event) {
            event.preventDefault();
            const itemType = event.dataTransfer.getData('text/plain');
            const areaType = dropArea.dataset.areaType;

            if (itemType === areaType) {
                const draggableItem = document.querySelector(`[data-item-type="${itemType}"] .emoji`);
                const textItems = document.querySelectorAll(`[data-item-type="${itemType}"] .food-text`);
                
                textItems.forEach(function(textItem) {
                    if (textItem.parentElement.querySelector('.emoji') === draggableItem) {
                        textItem.style.display = 'none'; // Hide the text associated with the matched draggableItem
                    }
                });
                
                draggableItem.style.fontSize = '20px';
                draggableItem.style.position = 'absolute';
                if (['grains', 'proteins', 'diary'].includes(areaType)) {
                    draggableItem.style.left = 'calc(50% - 150px)'; // Adjust as needed
                }

                dropArea.appendChild(draggableItem);
                event.target.classList.add('correct');
                score += 20;
                updateScoreDisplay(score);
                console.log('Current Score:', score);
            }
        });
    });

    // Rest of your code...
});
