deleteBtns = document.querySelectorAll(".delete-button");
for (let i = 0; i < deleteBtns.length; i++) {
  const deleteBtn = deleteBtns[i];
        deleteBtn.onclick = function(e) {
          console.log("Delete event: ", e);
          const venueId = e.target.dataset.id;
          fetch('/venues/'+ venueId + '/delete',{
            method: 'DELETE'
          }).then(function() {
            console.log('Parent?', e.target);
            const venue = e.target.parentElement;
            venue.remove();
            document.getElementById("error").className = "hidden";
          })
          .catch(function(e) {
            console.error(e);
            document.getElementById("error").className = "";
          });
        };
      }