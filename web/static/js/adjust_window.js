function setMainSectionHeight() {
            const header = document.querySelector('.header');
            const footer = document.querySelector('.footer');
            const main = document.querySelector('.main-section');

            const headerHeight = header?.offsetHeight || 0;
            const footerHeight = footer?.offsetHeight || 0;
            const vh = window.innerHeight;

            main.style.minHeight = `${vh - headerHeight - footerHeight}px`;
        }

        window.addEventListener('load', setMainSectionHeight);
        window.addEventListener('resize', setMainSectionHeight);