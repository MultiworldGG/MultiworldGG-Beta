const SPHERE_COLUMNS = ['sphere', 'finder', 'receiver', 'item', 'classification', 'location', 'game', 'checked_at'];
const SPHERE_FILTER_FIELDS = ['finder', 'receiver', 'game', 'sphere_min', 'sphere_max'];
const SPHERE_CLASSIFICATIONS = ['progression', 'useful', 'trap', 'filler'];
const SEARCH_DEBOUNCE_MS = 300;

const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[character]));

const renderClassification = (label) => {
    const primary = String(label).split(',')[0].trim();
    return `<span class="item-class item-class-${escapeHtml(primary)}">${escapeHtml(label)}</span>`;
};

const renderTimestamp = (seconds) => {
    if (seconds === null || seconds === undefined)
        return '<span class="item-class-filler">n/a</span>';
    const date = new Date(seconds * 1000);
    return `<time datetime="${date.toISOString()}" title="${date.toISOString()}">${date.toLocaleString()}</time>`;
};

const checkedClassifications = (form) =>
    Array.from(form.querySelectorAll('input[name="classification"]:checked')).map((box) => box.value);

// Filter params from the form; all-or-none classifications mean "no type filter".
const filterParams = (form) => {
    const params = new URLSearchParams();
    for (const name of SPHERE_FILTER_FIELDS) {
        const value = form.elements[name].value.trim();
        if (value)
            params.append(name, value);
    }
    const classifications = checkedClassifications(form);
    if (classifications.length && classifications.length < SPHERE_CLASSIFICATIONS.length) {
        classifications.forEach((value) => params.append('classification', value));
    }
    return params;
};

const applyUrlToForm = (form, params) => {
    for (const name of SPHERE_FILTER_FIELDS) {
        if (params.has(name))
            form.elements[name].value = params.get(name);
    }
    const classifications = params.getAll('classification');
    if (classifications.length) {
        form.querySelectorAll('input[name="classification"]').forEach((box) => {
            box.checked = classifications.includes(box.value);
        });
    }
};

// jQuery serialises array values as repeated keys only with `traditional: true`.
const toAjaxData = (params) => {
    const data = {};
    for (const [key, value] of params) {
        data[key] = key in data ? [].concat(data[key], value) : value;
    }
    return data;
};

window.addEventListener('load', () => {
    const wrapper = document.getElementById('tracker-wrapper');
    const form = document.getElementById('sphere-filters');
    const searchBox = document.getElementById('search');
    const csvLink = document.getElementById('csv-link');
    const rowsUrl = wrapper.dataset.rowsUrl;
    const csvUrl = wrapper.dataset.csvUrl;

    const initial = new URLSearchParams(location.search);
    applyUrlToForm(form, initial);
    searchBox.value = initial.get('q') || '';
    const initialSort = Math.max(SPHERE_COLUMNS.indexOf(initial.get('sort')), 0);
    const initialDir = initial.get('dir') === 'desc' ? 'desc' : 'asc';
    const initialLimit = parseInt(initial.get('limit'));

    const table = $('#sphere-table').DataTable({
        serverSide: true,
        processing: true,
        paging: true,
        pageLength: Number.isFinite(initialLimit) && initialLimit > 0 ? initialLimit : 100,
        lengthMenu: [50, 100, 250, 500, 1000],
        order: [[initialSort, initialDir]],
        search: { search: searchBox.value },
        dom: '<"sphere-table-controls"lip>rt<"sphere-table-controls"p>',
        language: {
            processing: 'Loading...',
            lengthMenu: '_MENU_ rows per page',
            info: 'Showing _START_ to _END_ of _TOTAL_ checks',
            infoEmpty: 'No checks',
            infoFiltered: '(filtered from _MAX_)',
            zeroRecords: 'No checked locations match the current filters.',
        },
        ajax: {
            url: rowsUrl,
            traditional: true,
            data: (request) => {
                const order = request.order[0] || { column: 0, dir: 'asc' };
                const params = filterParams(form);
                if (request.search.value)
                    params.set('q', request.search.value);
                params.set('sort', SPHERE_COLUMNS[order.column]);
                params.set('dir', order.dir);
                csvLink.href = `${csvUrl}?${params}`;

                params.set('limit', request.length);
                const url = new URL(location.href);
                url.search = params.toString();
                history.replaceState(null, '', url);

                params.set('offset', request.start);
                params.set('draw', request.draw);
                return toAjaxData(params);
            },
        },
        columns: [
            { data: 'sphere', className: 'number' },
            { data: 'finder', render: escapeHtml },
            { data: 'receiver', render: escapeHtml },
            { data: 'item', render: escapeHtml },
            { data: 'classification', render: renderClassification },
            { data: 'location', render: escapeHtml },
            { data: 'game', render: escapeHtml },
            { data: 'checked_at', render: renderTimestamp },
        ],
    });

    let searchTimer;
    searchBox.addEventListener('input', () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => table.search(searchBox.value).draw(), SEARCH_DEBOUNCE_MS);
    });
    searchBox.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && searchBox.value !== '') {
            searchBox.value = '';
            table.search('').draw();
            event.preventDefault();
        }
    });
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        table.draw();
    });
    // reset restores the controls after the event fires, so redraw on the next tick
    form.addEventListener('reset', () => setTimeout(() => table.draw(), 0));

    const targetSecond = (parseInt(wrapper.dataset.second) || 0) + 3;
    const getSleepTimeSeconds = () => ((((targetSecond - new Date().getSeconds()) % 60) + 60) % 60) || 60;
    let refreshOnView = false;
    let refreshTimer;
    const refresh = () => {
        if (document.hidden) {
            refreshOnView = true;
        } else {
            refreshOnView = false;
            table.ajax.reload(null, false);
        }
        refreshTimer = setTimeout(refresh, getSleepTimeSeconds() * 1000);
    };
    refreshTimer = setTimeout(refresh, getSleepTimeSeconds() * 1000);
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden && refreshOnView) {
            clearTimeout(refreshTimer);
            refresh();
        }
    });
});
