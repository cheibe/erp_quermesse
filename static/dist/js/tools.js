function fetchComTimeout(url, options = {}, timeout = 5000) {
    const controller = new AbortController();
    const signal = controller.signal;
    const timerId = setTimeout(() => {
        controller.abort();
    }, timeout);

    return fetch(url, { ...options, signal })
    .then(response => {
        clearTimeout(timerId);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .finally(() => {
        clearTimeout(timerId);
    });
}

export default fetchComTimeout;