document.querySelectorAll('.user-avatar').forEach(avatar => {

    const colors = [
        "#E53935",
        "#8E24AA",
        "#3949AB",
        "#1E88E5",
        "#00897B",
        "#43A047",
        "#F4511E",
        "#6D4C41",
        "#546E7A",
        "#FB8C00"
    ];

    const name = avatar.dataset.name;

    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash += name.charCodeAt(i);
    }

    avatar.style.backgroundColor = colors[hash % colors.length];

});
