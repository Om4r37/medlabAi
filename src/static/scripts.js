function closeFlash() {
    document.getElementById('flash').style.display = 'none';
    document.getElementsByTagName('main')[0].style.marginTop = '15px';
}
function highlight(childNo) {
    const navbarTabs = document.querySelectorAll('.navbar-tab');
    navbarTabs[childNo].classList.add('highlight');
    navbarTabs[childNo + 3].classList.add('highlight');
}