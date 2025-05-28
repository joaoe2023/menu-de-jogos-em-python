// Draw the hangman
function drawHangman() {
    stroke(255);
    strokeWeight(3);
    noFill();
    
    // Base
    line(100, 350, 300, 350);
    
    // Vertical pole
    line(200, 350, 200, 100);
    
    // Top beam
    line(200, 100, 300, 100);
    
    // Rope
    line(300, 100, 300, 150);
    
    // Draw body parts based on lives with animation
    if (game.state.lives < 6) {
        push();
        // Add swinging animation
        let swing = sin(game.state.animation) * 5;
        translate(swing, 0);
        
        // Head
        circle(300, 170, 40);
        
        if (game.state.lives < 5) {
            // Body
            line(300, 190, 300, 270);
        }
        
        if (game.state.lives < 4) {
            // Left arm
            line(300, 210, 260, 250);
        }
        
        if (game.state.lives < 3) {
            // Right arm
            line(300, 210, 340, 250);
        }
        
        if (game.state.lives < 2) {
            // Left leg
            line(300, 270, 260, 320);
        }
        
        if (game.state.lives < 1) {
            // Right leg
            line(300, 270, 340, 320);
        }
        
        // Add face when head is drawn
        if (game.state.lives < 6) {
            // Eyes
            fill(255);
            noStroke();
            circle(290, 165, 5);
            circle(310, 165, 5);
            
            // Sad mouth
            noFill();
            stroke(255);
            arc(300, 175, 20, 10, 0, PI);
        }
        
        pop();
    }
}

// Draw the word with guessed letters
function drawWord() {
    textAlign(CENTER);
    textSize(32);
    fill(255);
    noStroke();
    
    const wordDisplay = game.state.word.split('').map(letter => 
        game.state.guessedLetters.has(letter) ? letter : '_'
    ).join(' ');
    
    text(wordDisplay, width/2, 380);
}

// Draw the keyboard
function drawKeyboard() {
    // Keyboard is handled by HTML/CSS
} 