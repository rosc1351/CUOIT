var express = require('express')
var fileUpload = require('express-fileupload')
var bodyParser = require('body-parser')
var app = express()
var http = require('http').Server(app)
var io = require('socket.io')(http)
var path = require('path')
var xlsx = require('node-xlsx').default
var fs = require('fs')

// Local Requirements
var sheets = require('./sheets.js')

// App Settings
app.use(express.static(__dirname))
app.use(fileUpload())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
// Section Break

// Example get request (Send data TO user)
app.get('/test', (req, res) => {
  res.send('hello world')
})

// Example post request (Get data FROM user)
app.post('/test', (req, res) => {
  console.log(req.body)
  io.emit('gotdata', req.body)
  parseExcel()
  res.sendStatus(200)
})
// Section Break

// Get the sheet data from sheets.js and parse the columns
function getSheetData (callback) {
  sheets.fetch((sheetsData) => {
    console.log('raw data from google sheets')
    console.log(sheetsData.slice(0, 5))
    var time = sheetsData.map(function (row) {
      return row[0]
    })
    var checks = sheetsData.map(function (row) {
      return row[1]
    })
    var status = sheetsData.map(function (row) {
      return row[2]
    })
    callback(time, checks, status)
  })
}
// Get the most recent row for a given room
// Returns an array of size 2 as [date, status] of last check
function getLastCheck (times, checks, status, room) {
  var latestCheck = new Date(0)
  var lastStatus = 3
  for (var d in checks) {
    if (checks[d] === room) {
      if (latestCheck === null) {
        latestCheck = new Date(times[d])
        lastStatus = status[d]
      } else {
        var compareCheck = new Date(times[d])
        if (latestCheck < compareCheck) {
          latestCheck = compareCheck
          lastStatus = status[d]
        }
      }
    }
  } return [latestCheck, lastStatus]
}
// Handle browser request for table data
// Sources from sheet data and local excel file
// Returns a list of dictionaries for each room
// ######
// TODO (1): |liveData| < |checks| so 25 live data must be updated to include all rooms
app.get('/sheets', (req, res) => {
  getSheetData((times, checks, status) => {
    var table = []
    var liveData = parseExcel()

    // TODO (1)
    console.log('liveData:' + Object.keys(liveData).length)
    console.log('checks:' + (new Set(checks)).size)
    for (var r in liveData) {
      var x = getLastCheck(times, checks, status, r)
      var lastCheck = x[0]
      var st = x[1] // room status, 0=good, 1=low issue, 2=escalate
      table.push({
        roomName: r,
        status: st,
        booked: liveData[r],
        lastCheck: lastCheck,
        daysSince: (Date.now() - lastCheck) / (60 * 60 * 24 * 1000) // subtraction gives ms between 2 dates, division converts to days
      })
    } console.log(table.slice(0, 5))
    res.send(table)
  })
})

function parseExcel () {
  const workSheetsFromFile = xlsx.parse(`${__dirname}/myUploadedFile.xlsx`)
  var myDict = {}
  for (var i = 0; i < workSheetsFromFile[0].data.length - 2; i++) {
    if (workSheetsFromFile[0].data[i][0] === 'Event Times') {
      var roomName = workSheetsFromFile[0].data[i - 1][0]
      var events = []
      for (var j = i + 1; j < workSheetsFromFile[0].data.length; j++) {
        if (workSheetsFromFile[0].data[j][0] === 'Event Times') {
          for (var k = i + 1; k < j - 1; k++) {
            if (workSheetsFromFile[0].data[k].length > 0) {
              events.push(workSheetsFromFile[0].data[k][0])
            }
          }
          myDict[roomName] = events
          break
        }
      }
    }
  }
  return myDict
}

app.post('/file', function (req, res) {
  if (Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.')
  }
  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  let sampleFile = req.files.sampleFile
  // Use the mv() method to place the file somewhere on your server
  sampleFile.mv(path.join(__dirname, 'myUploadedFile.xlsx'), function (err) {
    if (err) {
      return res.status(500).send(err)
    }
    res.send('File uploaded!')
  })
})


io.on('connection', (socket) => {
  console.log('connection')
})

var server = http.listen(3000, () => {
  console.log('server is listening on', server.address().port)
})
