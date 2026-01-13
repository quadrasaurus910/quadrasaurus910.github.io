document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const mobileSidebarOverlay = document.getElementById('mobileSidebarOverlay');
    const dropdownItems = document.querySelectorAll('#mobileSidebarOverlay .dropdownItem');
    const body = document.body;

    // Function to open the mobile sidebar
    function openMobileSidebar() {
        body.classList.add('sidebar-open');
        // Apply staggered animation
        dropdownItems.forEach((element, index) => {
            element.style.transitionDelay = `${index * 50}ms`; // Stagger delay
            element.style.animation = 'none'; // Reset animation to re-trigger
            void element.offsetWidth; // Trigger reflow for animation reset
            element.style.animation = `fadeInSlideIn 0.3s ease-out forwards`;
        });
    }

    // Function to close the mobile sidebar
    function closeMobileSidebar() {
        // Apply staggered reverse animation
        // We need to reverse the order for a smooth "closing" effect
        const reversedItems = Array.from(dropdownItems).reverse();
        reversedItems.forEach((element, index) => {
            element.style.transitionDelay = `${index * 50}ms`; // Stagger delay
            element.style.animation = 'none'; // Reset animation
            void element.offsetWidth; // Trigger reflow
            element.style.animation = `fadeOutSlideOut 0.3s ease-in forwards`;
        });

        // After all items have animated out, remove the sidebar-open class
        // Use a timeout that matches the total animation time of the last item
        const totalAnimationTime = (dropdownItems.length * 50) + (300); // Items delay + animation duration
        setTimeout(() => {
            body.classList.remove('sidebar-open');
             // Reset transitionDelay for next open
            dropdownItems.forEach(element => element.style.transitionDelay = '0ms');
        }, totalAnimationTime);
    }

    // Event Listener for the Toggle Button
    sidebarToggleBtn.addEventListener('click', () => {
        if (body.classList.contains('sidebar-open')) {
            closeMobileSidebar();
        } else {
            openMobileSidebar();
        }
    });

    // Event Listener for clicking outside the sidebar to close it
    // Only applies when the mobile sidebar is active (screen < 600px)
    document.addEventListener('click', (event) => {
        const isClickInsideSidebar = mobileSidebarOverlay.contains(event.target);
        const isClickOnToggleButton = sidebarToggleBtn.contains(event.target);

        // Check if the sidebar is open AND the click was outside the sidebar and not on the toggle button
        if (body.classList.contains('sidebar-open') && !isClickInsideSidebar && !isClickOnToggleButton) {
            closeMobileSidebar();
        }
    });

    // Handle initial state and resize (no more direct style manipulation on resize)
    function handleResize() {
        // This function is mostly for showing / hiding the button based on media query capabilities
        // The CSS handles sidebar visibility, so JS just needs to ensure state is clean.
        if (window.innerWidth >= 600 && body.classList.contains('sidebar-open')) {
            // If we resize to medium/large while sidebar is open, close it cleanly
            closeMobileSidebar();
        }

        // testX element was for debugging, can be removed or used for other debugging
        // testX.innerHTML = window.innerWidth;
    }

    // Initial check on load
    handleResize();
    // Re-check on resize
    window.addEventListener('resize', handleResize);


    // Optional: Close sidebar if tab visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.hidden && body.classList.contains('sidebar-open')) {
            closeMobileSidebar();
        }
    });

    var more = document.querySelectorAll('#moreLess');
    var testButton = document.querySelector('#testButton');
    testButton.addEventListener('click', clickTest);

    function clickTest() {
        alert('clicked');
        // alert(event.target.children[0].innerhtml);
    }

    function toggleMore(event) {
        let more = event.target;
        let moreChildren = more.children;
        let moreText = moreChildren[0];
        let moreIcon = moreChildren[1];
        alert(moreText.innerHtml);
        if (moreText.innerHtml == 'MORE') {
            moreText.innerHtml == 'LESS';
        } else {
            moreText.innerHtml == 'MORE';
        }
    }

    // Optional: Scroll position logging (for debugging, can remove)
    // window.addEventListener("scroll", (event) => {
    //     document.querySelector('#testX').textContent = `scrollTop: ${window.scrollY}`;
    // });
});
