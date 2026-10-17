document.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-me-remove]');
    if (!button || !confirm(button.dataset.confirm)) return;
    button.disabled = true;
    let ok = false;
    try {
        ok = (await fetch(button.dataset.meRemove, { method: 'DELETE' })).ok;
    } catch (e) {}
    if (ok) {
        button.closest('.mw-card-cluster').remove();
    } else {
        button.disabled = false;
        alert('Could not delete. Reload the page and try again.');
    }
});
