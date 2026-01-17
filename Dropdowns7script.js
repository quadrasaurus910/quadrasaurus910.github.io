document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const mobileSidebarOverlay = document.getElementById('mobileSidebarOverlay');
    const dropdownItems = document.querySelectorAll('#mobileSidebarOverlay .dropdownItem');
    const body = document.body;

    function openMobileSidebar() {
        body.classList.add('sidebar-open');
        dropdownItems.forEach((element, index) => {
            element.style.transitionDelay = `${index * 50}ms`;
            element.style.animation = 'none';
            void element.offsetWidth;
            element.style.animation = `fadeInSlideIn 0.3s ease-out forwards`;
        });
    }

    function closeMobileSidebar() {
        const reversedItems = Array.from(dropdownItems).reverse();
        reversedItems.forEach((element, index) => {
            element.style.transitionDelay = `${index * 50}ms`;
            element.style.animation = 'none';
            void element.offsetWidth;
            element.style.animation = `fadeOutSlideOut 0.3s ease-in forwards`;
        });

        const totalAnimationTime = (dropdownItems.length * 50) + (300);
        setTimeout(() => {
            body.classList.remove('sidebar-open');
            dropdownItems.forEach(element => element.style.transitionDelay = '0ms');
        }, totalAnimationTime);
    }

    sidebarToggleBtn.addEventListener('click', () => {
        if (body.classList.contains('sidebar-open')) {
            closeMobileSidebar();
        } else {
            openMobileSidebar();
        }
    });

    document.addEventListener('click', (event) => {
        const isClickInsideSidebar = mobileSidebarOverlay.contains(event.target);
        const isClickOnToggleButton = sidebarToggleBtn.contains(event.target);
        if (body.classList.contains('sidebar-open') && !isClickInsideSidebar && !isClickOnToggleButton) {
            closeMobileSidebar();
        }
    });

    // NEW FUNCTION: Toggle Card Expansion
    window.toggleCard = function(btn) {
        const card = btn.closest('.card');
        const wrapper = card.querySelector('.expand-wrapper');
        const btnText = btn.querySelector('.btn-text');
        const icon = btn.querySelector('.material-icons');

        const isOpen = wrapper.classList.contains('is-open');

        if (isOpen) {
            wrapper.classList.remove('is-open');
            card.classList.remove('is-open-card');
            btnText.innerText = "MORE";
            icon.innerText = "expand_more";
        } else {
            wrapper.classList.add('is-open');
            card.classList.add('is-open-card');
            btnText.innerText = "LESS";
            icon.innerText = "expand_less";
        }
    };
});
