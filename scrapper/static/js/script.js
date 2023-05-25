$(document).ready(function() {
    $('#contactForm').submit(function(event) {
      console.log('button clicked');
      event.preventDefault();

      var name = $('#name').val();
      var email = $('#email').val();
      var subject = $('#subject').val();
      var message = $('#message').val();
      var role = $('#role').val();
      console.log(role);

      // Perform field validation
      if (name === '' || email === '' || subject === '' || message === '' || role === '') {
        // Display error message if any field is empty
        $('#success').text('Please fill in all fields.');
        $('#success').removeClass('success-message');
        $('#success').addClass('error-message'); // Apply error class to the success message element
        return;
      }
      if (!validateEmail(email)) {
        $('#success').text('Enter a valid email address!');
        $('#success').removeClass('success-message');
        $('#success').addClass('error-message'); // Apply error class to the success message element
        return;
      }
      var base_url = '{{ base_url }}';  // Add this line

      // Make an AJAX POST request to the backend endpoint
      $.ajax({
        type: 'POST',
        url: base_url + 'message',
        data: {
          name: name,
          email: email,
          subject: subject,
          role: role,
          message_body: message
        },
        dataType: "json",
        success: function(response) {
          // Display success message
          console.log('response is ' + response);
          $('#success').text('Message sent!');
          $('#success').addClass('success-message');
          $('#success').removeClass('error-message'); // Remove error class from the success message element
        },
        error: function(error) {
          console.log('error is ' + error);
          // Display error message
          $('#success').text('Error sending message.');
          $('#success').addClass('error-message'); // Apply error class to the success message element
          $('#success').removeClass('success-message'); // Remove success class from the success message element
        }
      });
    });
  });