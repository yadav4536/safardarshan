 // Function to handle image preview
 document.getElementById('pictures').addEventListener('change', function(event) {
    const file = event.target.files[0]; // Get the first selected file
    const imagePreview = document.getElementById('imagePreview');

    if (file) {
        const reader = new FileReader(); // Create a FileReader object
        reader.onload = function(e) {
            imagePreview.src = e.target.result; // Set the image source to the file's data URL
            imagePreview.style.display = 'block'; // Show the image preview
        };
        reader.readAsDataURL(file); // Read the file as a data URL
    } else {
        imagePreview.src = ''; // Reset the image preview if no file is selected
        imagePreview.style.display = 'none'; // Hide the image preview
    }
});





document.getElementById('category').addEventListener('change', function() {
    var category = this.value;
    var stateGroup = document.getElementById('state-group');
    var cityGroup = document.getElementById('city-group');
    
    // Show State input if 'city' is selected, hide otherwise
    if (category === 'city') {
        stateGroup.style.display = 'block';  // Show state input
        cityGroup.style.display = 'none';    // Hide city input
    } 
    // Show City input for other categories
    else if (category === 'restaurant' || category === 'hotel' || category === 'place') {
        stateGroup.style.display = 'none';   // Hide state input
        cityGroup.style.display = 'block';   // Show city input
    } 
    // Hide both if no category selected
    else {
        stateGroup.style.display = 'none';
        cityGroup.style.display = 'none';
    }
});