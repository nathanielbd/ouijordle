var socket = io()
var $startForm = $("#start")
var $controls = $('#controls')
var $nameField = $('#name')
var $game = $('#game')

var $shareLink = $('#shareLink')
var $roomCount = $('#roomCount')
var data = { 
    room: window.location.pathname.split('/')[1],
    name: null
}

var $names = $("#names")
var $players = $("#players")

var count = 0

$roomCount.text('0 players')

$startForm.on('submit', function(event) {
    event.preventDefault()
    data.name = $nameField.val()
    $startForm.hide()
    $controls.show()
    $nameField.blur()
    socket.emit('join', data)
})

socket.on('name_taken', function(data) {
    alert(`The name ${data.name} is taken in this room.`)
})

socket.on('join', function(data) {
    count++
    $players.append(`<span class="bubble">${data.name}</span>`)
    $names.append(`<span class="bubble">${data.name}</span>`)
})