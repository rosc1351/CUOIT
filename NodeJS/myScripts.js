var minimizeButtons = document.querySelectorAll('a.sectionButton')

console.log('buttons:')
console.log(minimizeButtons)

console.log('Hello World')

minimizeButtons.forEach(function (element) {
  console.log(element)
  element.onclick = function (e) {
    e.preventDefault()
    console.log('clicked')
    var sectionHeader = element.parentElement
    var card = sectionHeader.parentElement
    var sectionContent = card.querySelector('.sectionContent')
    if (sectionContent.style.display === 'none') {
      sectionContent.style.display = 'block'
    } else {
      sectionContent.style.display = 'none'
    }

    console.log(sectionContent)
  }
})
