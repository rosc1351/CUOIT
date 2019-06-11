var myTable
window.onload = function () {
  myTable = $('#dataTable').DataTable({
    "ordering": true,
    "scrollX": true
  })
  console.log($('.dataTable'))
  console.log("done")
}

function addRow (content) {
  var row = myTable.row.add([content.roomName, content.status, content.booked, content.lastCheck, Math.floor(content.daysSince)]).draw().node()

  row.onclick = function () {
    console.log(row.className)
    if (row.style.backgroundColor === 'red') {
      if (row.className === 'odd') {
        $(row).css('background-color', '#333333')
      } else {
        $(row).css('background-color', '#232323')
      }
    } else {
      $(row).css('background-color', 'red')
      console.log('click')
    }
  }

  row.onenter = function () {
    $(row).css('background-color', 'red')
  }
}

function clearTable () {
  myTable.clear().draw()
}

document.querySelector('#clearTableButton').onclick = function () {
  clearTable()
}


var socket = io()

socket.on('gotdata', function () {
  console.log('got confirm')
})

function postData (pData) {
  $.post('http://royceschultz.com/test', pData)
}

function getData () {
  $.get('http://royceschultz.com/test', (data) => {
    console.log(data)
  })
}

document.querySelector('#testButton').onclick = function () {
  getData()
  addRow()
}

document.querySelector('#testButton2').onclick = function () {
  postData('posting Data')
}


function getSheetsData () {
  $.get('http://royceschultz.com/sheets', (data) => {
    for (var d in data) {
      addRow(data[d])
    }
  })
}

document.querySelector('#getSheetsButton').onclick = function () {
  myTable.clear().draw()
  getSheetsData()
}
