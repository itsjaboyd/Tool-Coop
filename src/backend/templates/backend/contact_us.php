<?php

if($_POST["submit"]) {
    $recipient="AboutUs@LuckyMail.com";
    $subject="Form to email message";
    $sender=$_POST["firstname"] + " " + $_POST["lastname"];
    $senderEmail=$_POST["email"];
    $message=$_POST["subject"];

    $mailBody="Name: $sender\nEmail: $senderEmail\n\n$message";

    mail($recipient, $subject, $mailBody, "From: $sender <$senderEmail>");

    $thankYou="<p>Thank you! Your message has been sent.</p>";
}

?>

<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

    <title>Toolshed!</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta http-equiv="refresh" content="5;URL=./contact_us.html">
  </head>
  <body>
	<?=$thankYou ?>
	
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <a class="navbar-brand" href="#">Toolshed</a>
    
      <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
        <ul class="navbar-nav mr-auto ml-5 mt-2 mt-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Check Out Tools</a>
          </li>
          <li class="nav-item">
              <a class="nav-link" href="{% url 'inventory' %}">Inventory</a>
          </li>
		  <li class="nav-item active">
              <a class="nav-link" href="{% url 'contact_us' %}">Contact Us</a>
          </li>
        </ul>
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          {% if user.is_authenticated%}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'profile' %}">View Profile</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'logout' %}">Logout</a>
          </li>
          {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'login' %}">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'register' %}">Register</a>
          </li>
          {% endif %}
        </ul>
      </div>
    </nav>
		
	
	
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
  </body>
</html>