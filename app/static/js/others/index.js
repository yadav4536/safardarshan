 // Automatically hide flash messages after 5 seconds (5000 ms)
 setTimeout(function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        // Use Bootstrap's fade-out effect by removing 'show' class
        alert.classList.remove('show');
        // Remove the element from DOM after the fade-out transition (500ms for Bootstrap 5 alerts)
        setTimeout(function() {
            alert.remove();
        }, 500); // Delay for fade out transition
    });
}, 3000); // 3 seconds



let scrollInterval;  // Declare scrollInterval globally
        
        // Start scrolling
        function startAutoScroll() {
            const scrollContainer = document.querySelector('.scroll-container');
        
            // Set interval for continuous scrolling
            scrollInterval = setInterval(() => {
                scrollContainer.scrollLeft += 1;  // Adjust scroll speed
            }, 20);  // Interval time for scrolling speed
        
            // Stop scrolling on hover
            scrollContainer.addEventListener('mouseenter', stopAutoScroll);
        
            // Resume scrolling when the mouse leaves
            scrollContainer.addEventListener('mouseleave', startAutoScroll);
        }
        
        // Stop auto-scroll when hovering
        function stopAutoScroll() {
            clearInterval(scrollInterval);  // Stop the interval
        }
        
        // Start auto-scroll when the page loads
        window.onload = startAutoScroll;












        document.getElementById('search').addEventListener('input', function() {
            const query = this.value;
        
            if (query.length < 3) {  // Start suggesting only after 3 characters
                document.getElementById('suggestions').innerHTML = '';
                document.getElementById('suggestions').style.display = 'none';
                return;
            }
        
            fetch(`/suggestions?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    const suggestionsBox = document.getElementById('suggestions');
                    suggestionsBox.innerHTML = ''; // Clear previous suggestions
        
                    // Loop through all suggestion categories and display them
                    const categories = ['cities', 'restaurants', 'hotels', 'places'];
                    categories.forEach(category => {
                        data[category].forEach(item => {
                            const div = document.createElement('div');
                            div.textContent = item;
                            div.onclick = () => {
                                document.getElementById('search').value = item; // Set input value
                                suggestionsBox.innerHTML = ''; // Clear suggestions
                                suggestionsBox.style.display = 'none'; // Hide suggestions
                            };
                            suggestionsBox.appendChild(div);
                        });
                    });
        
                    // Display suggestions if any
                    if (suggestionsBox.childNodes.length > 0) {
                        suggestionsBox.style.display = 'block';
                    } else {
                        suggestionsBox.style.display = 'none';
                    }
                });
        });


       