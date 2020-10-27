    document.getElementById('form').onsubmit = function (e) {
        e.preventDefault();
        fetch('/artist/create', {
            method: 'POST',
            body: JSON.stringify({
                'name': document.getElementById('form.name').value,
                'state': document.getElementById('form.state').value,
                'city': document.getElementById('form.city').value,
                'phone': document.getElementById('form.phone').value,
                'address': document.getElementById('form.address').value,
                'image_link': document.getElementById('form.image_link').value,
                'genres': document.getElementById('form.genres').value,
                'facebook_link': document.getElementById('form.facebook_link').value,
                'website': document.getElementById('form.website').value,
                'seeking_talent': document.getElementById('form.seeking_talent').checked,
                'seeking_description': document.getElementById('form.seeking_description').value
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

    }
