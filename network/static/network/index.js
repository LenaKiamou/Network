async function like_unlike(id) {
    like_button = document.getElementById(`like-button${id}`);
    
    if (like_button.style.backgroundColor == 'white') {
        await fetch(`../like_unlike/${id}`, {
            method:'PUT',
            body: JSON.stringify({
                like: true
            }) 
        });
        like_button.style.backgroundColor = 'blue';
        like_button.style.color = 'white';
    }
    else {
        await fetch(`../like_unlike/${id}`, {
            method:'PUT',
            body: JSON.stringify({
                like: false
            })
        });
        like_button.style.backgroundColor = 'white';
        like_button.style.color = 'black';
        
    }

    await fetch(`../like_unlike/${id}`)
    .then(response => response.json())
    .then(post => {
        like_button.innerHTML = post.likes;
    });

}


function edit(id) {
    edit_text = document.getElementById(`edit-text${id}`);
    edit_button = document.getElementById(`edit-button${id}`);
    save_button = document.getElementById(`save-button${id}`);
    cancel_button = document.getElementById(`cancel-button${id}`)
    edit_view = document.getElementById(`edit-view${id}`);
    post_content = document.getElementById(`post-content${id}`);

    edit_view.style.display = 'block';
    edit_button.style.display = 'none';
    post_content.style.display = 'none';

    cancel_button.addEventListener('click', () => {
        document.getElementById(`edit-view${id}`).style.display = 'none';
        edit_button.style.display = 'block';
        post_content.style.display = 'block';
    });

    save_button.addEventListener('click', () => {
        fetch(`/edit/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                description: edit_text.value
            })
        });
        edit_view.style.display = 'none';
        edit_button.style.display = 'block';
        post_content.style.display = 'block';

        document.getElementById(`post-content${id}`).innerHTML = edit_text.value;
    });
 
}


function follow_unfollow(flag) {
    const a = document.querySelector("#user_name").innerText;
    fetch(`../follow_unfollow/${flag}/${a}`)
        .then(response => response.json())
        .then(result => {
            if (result["flag"] == "unfollow") {
                document.querySelector('#follow').style.display = 'block';
                document.querySelector('#unfollow').style.display = 'none';
                document.querySelector("#num_Followers").innerHTML = `Followers: ${result.num}`
            }
            if (result["flag"] == "follow") {
                document.querySelector('#follow').style.display = 'none';
                document.querySelector('#unfollow').style.display = 'block';
                document.querySelector("#num_Followers").innerHTML = `Followers: ${result.num}`
            }  
    })
}


    