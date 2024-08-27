document.addEventListener('DOMContentLoaded', () => {
  const JSCarousel = ({
    carouselSelector,
    slideSelector,
    enablePagination = true,
    enableAutoplay = true,
    autoplayInterval = 3000,
  }) => {
    /*
     * Initialize variables to keep track of carousel state and
     * references to different elements.
     */
    let currentSlideIndex = 0;
    let prevBtn, nextBtn;
    let autoplayTimer;
    let paginationContainer;
  
    // Find the carousel element in the DOM.
    const carousel = document.querySelector(carouselSelector);
    console.log('carousel:>>>')
    console.log(carousel)
  
    // If carousel element is not found, log an error and exit.
    if (!carousel) {
      console.error("Specify a valid selector for the carousel.");
      return null;
    }
  
    // Find all slides within the carousel
    const slides = carousel.querySelectorAll(slideSelector);
    console.log("slides:>>>>")
    console.log(slides)
    console.log('slides length:>>>>')
    console.log(slides.length)
  
    if (!slides.length) {
      console.error("Specify a valid selector for slides.");
      return null;
    }
    
    // fn to add elements to DOM
    const addElement = (tag, attributes, children) => {
      const element = document.createElement(tag);
  
      if (attributes) {
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
  
    /*
     * Modify the DOM structure and add required containers and controls
     * to the carousel element.
     */
    const tweakStructure = () => {
      carousel.setAttribute("tabindex", "0");
  
      // Create a div for carousel inner content.
      const carouselInner = addElement("div", {
        class: "carousel-inner",
      });
      carousel.insertBefore(carouselInner, slides[0]);
  
      // If pagination is enabled, create and append pagination buttons.
      if (enablePagination) {
        paginationContainer = addElement("nav", {
          class: "carousel-pagination",
          role: "tablist",
        });
        carousel.appendChild(paginationContainer);
      }
  
      /*
       * Move slides from the carousel element to the carousel inner
       * container to facilitate alignment.
       */
      slides.forEach((slide, index) => {
        carouselInner.appendChild(slide);
        slide.style.transform = `translateX(${index * 100}%)`;
        if (enablePagination) {
          const paginationBtn = addElement(
            "button",
            {
              class: `carousel-btn caroursel-btn--${index + 1} paginate`,
              role: "tab",
            },
            `${index + 1}`
          );
  
          paginationContainer.appendChild(paginationBtn); // nav > button
  
  
          if (index === 0) {
            paginationBtn.classList.add("carousel-btn--active");
            paginationBtn.setAttribute("aria-selected", true);
          }
  
          paginationBtn.addEventListener("click", () => {
            handlePaginationBtnClick(index);
          });
        }
      });
  
      // Create and append previous button.
      prevBtn = addElement(
        "button",
        {
          class: "carousel-btn carousel-btn--prev-next carousel-btn--prev",
          "aria-label": "Previous Slide",
        },
        "<"
      );
      carouselInner.appendChild(prevBtn);
  
      // Create and append next button.
      nextBtn = addElement(
        "button",
        {
          class: "carousel-btn carousel-btn--prev-next carousel-btn--next",
          "aria-label": "Next Slide",
        },
        ">"
      );
      carouselInner.appendChild(nextBtn);
  
    };
  
    // Adjust slide positions according to the currently selected slide.
    const adjustSlidePosition = () => {
      slides.forEach((slide, i) => {
        slide.style.transform = `translateX(${100 * (i - currentSlideIndex)}%)`;
      });
    };
  
    /*
     * Update the state of pagination buttons according to the currently
     * selected slide.
     */
    const updatePaginationBtns = () => {
      const paginationBtns = paginationContainer.children;
      console.log("Pagination children:>>>");
      console.log(paginationBtns);
      const prevActiveBtns = Array.from(paginationBtns).filter((btn) =>
        btn.classList.contains("carousel-btn--active")
      );
      prevActiveBtns.forEach((btn) => {
        btn.classList.remove("carousel-btn--active");
        btn.removeAttribute("aria-selected");
      });
  
      console.log("current slide index:>>>");
      console.log(currentSlideIndex);
      const currActiveBtns = paginationBtns[currentSlideIndex];
      if (currActiveBtns) {
        currActiveBtns.classList.add("carousel-btn--active");
        currActiveBtns.setAttribute("aria-selected", true);
      }
    };
  
    // Update the overall carousel state.
    const updateCarouselState = () => {
      if (enablePagination) {
        updatePaginationBtns();
      }
      adjustSlidePosition();
    };
  
    // Move slide left and right based on direction provided.
    const moveSlide = (direction) => {
      const newSlideIndex =
        direction === "next"
          ? (currentSlideIndex + 1) % slides.length
          : (currentSlideIndex - 1 + slides.length) % slides.length;
      currentSlideIndex = newSlideIndex;
      updateCarouselState();
    };
  
    // Event handler for pagination button click event.
    const handlePaginationBtnClick = (index) => {
      currentSlideIndex = index;
      updateCarouselState();
    };
  
    // Event handlers for previous and next button clicks.
    const handlePrevBtnClick = () => {
      console.log('Previous button clicked')
      moveSlide("prev")
    };
    const handleNextBtnClick = () => {
      console.log('Next button clicked')
      moveSlide("next")
    };
  
    // Start autoplaying of slides.
    const startAutoplay = () => {
      autoplayTimer = setInterval(() => {
        moveSlide("next");
      }, autoplayInterval);
    };
  
    // Stop autoplaying of slides.
    const stopAutoplay = () => clearInterval(autoplayTimer);
  
    /* Event handlers to manage autoplaying intelligentally on mouse
     * enter and leave events.
     */
    const handleMouseEnter = () => stopAutoplay();
    const handleMouseLeave = () => startAutoplay();
  
    // Event handler for keyboard navigation.
    const handleKeyboardNav = (event) => {
      // Exit, if carousel is not the event target.
      if (!carousel.contains(event.target)) return;
      // Exit, if the default action on the event is already prevented.
      if (event.defaultPrevented) return;
  
      /*
       * Move slides in the respective directions when left and right
       * keys are pressed.
       */
      switch (event.key) {
        case "ArrowLeft":
          moveSlide("prev");
          break;
        case "ArrowRight":
          moveSlide("next");
          break;
        default:
          return;
      }
  
      /*
       * Stop the default actions of the event in question when the
       * carousel is the event target.
       */
      event.preventDefault();
    };
  
    // Attach event listeners to relevant elements.
    const attachEventListeners = () => {
      prevBtn.addEventListener("click", handlePrevBtnClick);
      nextBtn.addEventListener("click", handleNextBtnClick);
      carousel.addEventListener("keydown", handleKeyboardNav);
  
      if (enableAutoplay && autoplayInterval !== null) {
        carousel.addEventListener("mouseenter", handleMouseEnter);
        carousel.addEventListener("mouseleave", handleMouseLeave);
      }
    };
  
    // Initialize/create the carousel.
    const create = () => {
      tweakStructure();
      attachEventListeners();
      if (enableAutoplay && autoplayInterval !== null) {
        startAutoplay();
      }
    };
  
    // Destroy the carousel/clean-up.
    const destroy = () => {
      // Remove event listeners.
      prevBtn.removeEventListener("click", handlePrevBtnClick);
      nextBtn.removeEventListener("click", handleNextBtnClick);
      carousel.removeEventListener("keydown", handleKeyboardNav);
      if (enablePagination) {
        const paginationBtns = paginationContainer.querySelectorAll(".carousel-btn");
        if (paginationBtns.length) {
          paginationBtns.forEach((btn) => {
            btn.removeEventListener("click", handlePaginationBtnClick);
          });
        }
      }
  
      // Clear autoplay intervals if autoplay is enabled.
      if (enableAutoplay && autoplayInterval !== null) {
        carousel.removeEventListener("mouseenter", handleMouseEnter);
        carousel.removeEventListener("mouseleave", handleMouseLeave);
        stopAutoplay();
      }
    };
  
    // Return an object with methods to create and destroy the carousel.
    return { create, destroy };
  };
  
  const carousel1 = JSCarousel({
    carouselSelector: ".carousel",
    slideSelector: ".slide",
    enablePagination: true,
  });
  
  carousel1.create();
  window.addEventListener("unload", () => {
    carousel1.destroy();
  });

})

// TODO add event listener for window unload
// TODO add event listener for enter key on carousel item
// TODO 

