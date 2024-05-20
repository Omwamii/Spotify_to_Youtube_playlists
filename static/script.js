$(document).ready(() => {
    // console.log('Content loaded');

    // const spPlaylistSongsList = document.getElementById('spotify-tracks');
    // const songsArray = spPlaylistSongsList.dataset.tracks

    // console.log(songsArray);
    // add event listeners to remove items from array when de-selected
    $('.close-icon').on('click', () => {
        alert('close icon clicked');
    })


    const carouselController = (carouselSelector, slideSelector) => {
        const carousel = document.querySelector(carouselSelector);
        if (!carousel) {
            return null;
        }
        
        const slides = carousel.querySelectorAll(slideSelector);
        if (!slides.length) {
            return null;
        }
        let currentSlideIndex = 0;
        let prevBtn, nextBtn;
    }

   

      slides.forEach((slide, index) => {
        carouselInner.appendChild(slide);
        slide.style.transform = `translateX(${index * 100}%)`;
      });

      prevButton = addElement(
        "button",
        {
          class: "carousel-btn carousel-btn--prev-next carousel-btn--prev",
          "aria-label": "Previous Slide",
        },
        "<"
      );
      carouselInner.appendChild(prevButton);
    
      nextButton = addElement(
        "button",
        {
          class: "carousel-btn carousel-btn--prev-next carousel-btn--next",
          "aria-label": "Next Slide",
        },
        ">"
      );
      carouselInner.appendChild(nextButton);

     
      const updateCarouselState = () => {
        adjustSlidePosition();
      };

      const moveSlide = (direction) => {
        const newSlideIndex =
          direction === "next"
            ? (currentSlideIndex + 1) % slides.length
            : (currentSlideIndex - 1 + slides.length) % slides.length;
        currentSlideIndex = newSlideIndex;
        updateCarouselState();
      };

      const handlePrevButtonClick = () => moveSlide("prev");
      const handleNextButtonClick = () => moveSlide("next");

      const attachEventListeners = () => {
        prevButton.addEventListener("click", handlePrevButtonClick);
        nextButton.addEventListener("click", handleNextButtonClick);
      };

      const JSCarousel = ({}) => {
        const addElement = (tag, attributes, children) => {
          const element = document.createElement(tag);
    
          if (attributes) {
            // Set attributes to the element.
            Object.entries(attributes).forEach(([key, value]) => {
              element.setAttribute(key, value);
            });
          }
    
          if (children) {
            // Set content to the element.
            if (typeof children === "string") {
              element.textContent = children;
            } else {
              children.forEach((child) => {
                if (typeof child === "string") {
                  element.appendChild(document.createTextNode(child));
                } else {
                  element.appendChild(child);
                }
              });
            }
          }
    
          return element;
        };

        const tweakStructure = () => {
          const carouselInner = addElement("div", {
            class: "carousel-inner",
          });
          carousel.insertBefore(carouselInner, slides[0]);
        }

        const adjustSlidePosition = () => {
          slides.forEach((slide, i) => {
            slide.style.transform = `translateX(${100 * (i - currentSlideIndex)}%)`;
          });
        };

        const create = () => {
          tweakStructure();
          attachEventListeners();
        };
  
        const destroy = () => {
          prevBtn.removeEventListener("click", handlePrevBtnClick);
          nextBtn.removeEventListener("click", handleNextBtnClick);
        };

      //   enablePagination = (true,
      // }) => {
      //   // ...
      // };
        return {create, destroy};
      }
      
      // Initializing the first carousel
      const carousel1 = JSCarousel({
        carouselSelector: '#carousel-1',
        slideSelector: '.slide',
      });
      
      carousel1.create();
      
      // Cleanup
      //TODO replace unload event listener
      window.addEventListener('unload', () => {
        carousel1.destroy();
      });

      // Event handler for pagination button click event.
      const handlePaginationBtnClick = (index) => {
        currentSlideIndex = index;
        updateCarouselState();
};
})