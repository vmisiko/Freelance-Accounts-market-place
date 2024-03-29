
 <section class=" mb-4 mt-4 pt-5">

      <!--Grid row-->
      <div class="row wow fadeIn">
        <div class ="col-6 offset-3 ">

        <h1>{% trans "Sign Out" %}</h1>

        <p>{% trans 'Are you sure you want to sign out?' %}</p>

        <form method="post" action="{% url 'account_logout' %}">
          {% csrf_token %}
          {% if redirect_field_value %}
          <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}"/>
          {% endif %}
          <button type="submit"  class = "btn btn-primary">{% trans 'Sign Out' %}</button>
        </form>
        <hr class = "pb-3">

      </div>
    </div>
  </section>