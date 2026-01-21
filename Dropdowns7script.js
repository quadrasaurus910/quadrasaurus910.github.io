document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const mobileSidebarOverlay = document.getElementById('mobileSidebarOverlay');
    const dropdownItems = document.querySelectorAll('.dropdownItem');
    const body = document.body;

    /**
     * Mobile Sidebar Logic
     */
    function openMobileSidebar() {
        body.classList.add('sidebar-open');
        // Reset and trigger staggered fade-in for list items
        dropdownItems.forEach((element, index) => {
            element.style.animation = 'none';
            void element.offsetWidth; // Trigger reflow
            element.style.animation = `fadeInSlideIn 0.4s ease-out ${index * 50}ms forwards`;
        });
    }

    function closeMobileSidebar() {
        // Simple class removal handles the overlay and content slide-out via CSS
        body.classList.remove('sidebar-open');
        dropdownItems.forEach(el => el.style.animation = 'none');
    }

    sidebarToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (body.classList.contains('sidebar-open')) {
            closeMobileSidebar();
        } else {
            openMobileSidebar();
        }
    });

    // Close mobile sidebar when clicking the dark overlay area
    mobileSidebarOverlay.addEventListener('click', (e) => {
        if (e.target === mobileSidebarOverlay) {
            closeMobileSidebar();
        }
    });

    /**
     * Content Expansion Logic (Block 2)
     */
    window.toggleCard = function(btn) {
        const card = btn.closest('.card');
        const wrapper = card.querySelector('.expand-wrapper');
        const btnText = btn.querySelector('.btn-text');
        const icon = btn.querySelector('.material-icons');

        const isOpen = wrapper.classList.contains('is-open-wrapper');

        if (isOpen) {
            // Contract
            wrapper.classList.remove('is-open-wrapper');
            card.classList.remove('is-open-card');
            btnText.innerText = "MORE";
            icon.innerText = "expand_more";
            
            // Optional: Smooth scroll back to top of card if it's now out of view
            card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            // Expand
            wrapper.classList.add('is-open-wrapper');
            card.classList.add('is-open-card');
            btnText.innerText = "LESS";
            icon.innerText = "expand_less";
        }
    };

    /**
     * Responsive Cleanup
     */
    window.addEventListener('resize', () => {
        // If user expands screen to desktop size, force close mobile menu
        if (window.innerWidth >= 769 && body.classList.contains('sidebar-open')) {
            closeMobileSidebar();
        }
    });
});
