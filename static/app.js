let score = 0
let gameCount
let highScore
let timer
let gameStarted = false
let foundWords = []
const alertArea = $('#alert-area')


$('#start-button').on('click', async function() {
    gameStarted = true
    $('#score').html('0')
    $('#words-list').html('')
    alertArea.html('')
    clearInterval(timer)
    setTimer()
})

$('#new-game-button').on('click', function() {
    location.reload()
    $('#game-container').show()
})

$('#guess-form').on('submit', async function(evt) {
    evt.preventDefault();
    if (gameStarted === false) {
        return alertArea.html("<div class='alert alert-info mt-3' role='alert'>Click Start Game to play!</div>")
    }

    else {
        await checkWord();
        
        generateAlertResponse(result)

        if (result === 'ok' && !foundWords.includes(word)) {
            updateScore(word)
            foundWords.push(word)
            $('#words-list').empty()
            generateWordList()
        } 
        
        $('input[name=word').val('')
    }
})

async function checkWord() {
    bodyFormData = new FormData()
    word = $('#word-input').val()
    bodyFormData.set('word', word)
    response = await axios({      
        url: 'http://127.0.0.1:5000/word-check',
        method: 'POST',
        data: bodyFormData
    })
    result = response.data['result']
    return result
}

function generateAlertResponse(result) {
    if (result === 'ok') {
        if (foundWords.includes(word)) {
            return alertArea.html("<div class='alert alert-warning mt-3' role='alert'>You already guessed that word!</div>")
        }
        else {
            return alertArea.html("<div class='alert alert-success w-50 mt-3' role='alert'>Great Job!</div>")
        }
    }
    else if (result === 'not-on-board') {
        return alertArea.html("<div class='alert alert-danger w-50 mt-3' role='alert'>Word Not Found</div>")
    }
    else if (result === 'not-word') {
        return alertArea.html("<div class='alert alert-danger w-50 mt-3' role='alert'>Not Valid Word</div>")
    }
}

function updateScore(word) {
    score += word.length
    $('#score').html(score)
}

async function setTimer(){
    let sec = 60;
    timer = setInterval(async function(){
        $('#timer').html(`${sec}`)
        sec--;
        if (sec < 0) {
            clearInterval(timer);
            gameStarted = false
            
            alertArea.html(`<div class='alert alert-secondary w-50 mt-3' role='alert'>Game Over</div>`)
            response = await sendDataToServer()
            gameCount = response.game_count
            highScore = response.high_score
            $('#game-count').html(gameCount)
            $('#high-score').html(highScore)

            alert(`Game Over! Your score was ${score}`)
        }
    }, 1000);
}

function generateWordList() {
    for (let word of foundWords) {
        $('#words-list').append(`<li class='list-group-item'>${word}</li>`)
    }
}

async function sendDataToServer () {
    bodyFormData = new FormData()
    bodyFormData.set('score', score)
    response = await axios({      
        url: 'http://127.0.0.1:5000/store-data',
        method: 'POST',
        data: bodyFormData
    })
    
    result = response.data
    return result

}

