    document.getElementById('form').onsubmit = function (e) {
        e.preventDefault();
        fetch('/shows/create', {
            method: 'POST',
            body: JSON.stringify({
                'artist_id': document.getElementById('form.artist_id').value,
                'venue_id': document.getElementById('form.venue_id').value,
                'start_time': document.getElementById('form.start_time').value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(function (response) {
            return response.json();
        })
        // .then(function (jsonResponse) {
        //     const liItem = document.createElement('LI');

        //     liItem.innerHTML = jsonResponse['description'];
        //     document.getElementById('todos').appendChild(liItem);
        //     document.getElementById('error').className = 'hidden';
        //     window.location.reload(true);
        // })
        .catch(function () {
            document.getElementById('error').className = '';
        })
    }
