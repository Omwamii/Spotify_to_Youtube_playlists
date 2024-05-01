$(document).ready(() => {
    console.log('Content loaded');

    const spPlaylistSongsList = document.getElementById('spotify-tracks');
    const songsArray = spPlaylistSongsList.dataset.tracks

    console.log(songsArray);
    // add event listeners to remove items from array when de-selected
    $('.close-icon').on('click', () => {
        alert('close icon clicked');
    })

    const carousel = document.querySelector('.carousel');
    let isThrottled = false;

    function throttle(callback, limit) {
        let waiting = false;
        return function () {
            if (!waiting) {
                callback.apply(this, arguments);
                waiting = true;
                setTimeout(() => {
                    waiting = false;
                }, limit);
            }
        };
    }

    function handleScroll() {
        if (!isThrottled) {
            if (window.scrollY > window.innerHeight / 2) {
                carousel.style.transform = 'translateX(-100%)';
            } else {
                carousel.style.transform = 'translateX(0)';
            }
            isThrottled = true;
            setTimeout(() => {
                isThrottled = false;
            }, 500); // Adjust throttle timing as needed
        }
    }

    document.addEventListener('scroll', throttle(handleScroll, 200));
})