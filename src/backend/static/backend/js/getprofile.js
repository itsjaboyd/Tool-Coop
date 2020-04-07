$( "#other" ).change(function() {
    $.ajax({
      url:  'get-profile/'+ $( this ).value(),
      type:  'get',
      dataType:  'json',
      success: function  (data) {
          let rows =  '';
          profile = data.profile
          profile_info= `
          <hr>
          <h5 class="font-weight-bold"><u>Customer Information</u></h5>
          <!--Grid row-->
          <span class="font-weight-bold"> Address:</span>
          <div class="text-left ml-3">
            <p>{{ user.first_name }} {{ user.last_name}}
              <br>
              {{ profile.address1 }}, {{ profile.address2 }}
              <br>
              {{ profile.city }}, {{ profile.state }}
            </p>
          </div>
          <p>
              <span class="font-weight-bold"> Phone:</span> 
              {{ profile.phone }} 
          </p>
          <a class="btn btn-md btn-primary" href="{% url 'edit-profile' %}"> Update Profile </a>
          <hr>`;
          $('[#userInfo](https://paper.dropbox.com/?q=%23myTable) > tbody').append(rows);
      }
  });
});