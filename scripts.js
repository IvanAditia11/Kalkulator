const button_number = document.querySelectorAll('.number')
const secondary_display = document.getElementById('secondary-display')
const primary_display = document.getElementById('primary-display')

button_number.forEach((item) => {
    item.addEventListener('click', (e) => {
        secondary_display.textContent += e.target.textContent
    })
});


const addition = () => {
    const secondary_value = secondary_display.textContent
    primary_display.textContent += secondary_value
    primary_display.textContent += ' + '
}