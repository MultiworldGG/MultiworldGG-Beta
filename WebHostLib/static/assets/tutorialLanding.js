const COOKIE_NAME = 'show_hidden_games';

function setCookie(name, value, days = 365) {
  const expires = new Date(Date.now() + days*864e5).toUTCString();
  document.cookie = `${name}=${value};expires=${expires};path=/`;
}

function getCookie(name) {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='))
    ?.split('=')[1];
}

function updateNSFWVisibility() {
  const show = getCookie(COOKIE_NAME) === 'true';
  document.querySelectorAll('.tutorial-section[data-nsfw="true"]').forEach((el) => {
    el.style.display = show ? '' : 'none';
  });
  document.getElementById('toggle-nsfw').textContent = show
    ? 'Hide NSFW games'
    : 'Show NSFW games';
}

window.addEventListener('load', () => {
  const toggleLink = document.getElementById('toggle-nsfw');
  toggleLink.addEventListener('click', e => {
    e.preventDefault();
    const currently = getCookie(COOKIE_NAME) === 'true';
    setCookie(COOKIE_NAME, !currently);
    updateNSFWVisibility();
  });

  updateNSFWVisibility();

  // Check if we are on an anchor when coming in, and scroll to it.
  const hash = window.location.hash;
  if (hash) {
    // Use a small delay to ensure DOM is fully rendered and filtering applied
    setTimeout(() => {
      const targetId = hash.slice(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
        // Make sure the target element is visible (not hidden by NSFW filter)
        const tutorialSection = targetElement.closest('.tutorial-section');
        if (tutorialSection && tutorialSection.style.display === 'none') {
          // If the target is hidden by NSFW filter, show NSFW content temporarily
          const wasShowing = getCookie(COOKIE_NAME) === 'true';
          if (!wasShowing) {
            setCookie(COOKIE_NAME, 'true');
            updateNSFWVisibility();
          }
        }
        
        // Scroll to the target element
        const offset = 128;  // To account for navbar banner at top of page.
        const scrollTop = targetElement.offsetTop - offset;
        window.scrollTo(0, scrollTop);
      }
    }, 100); // Small delay to ensure DOM is ready
  }
});
