$(document).ready(function() {
    $('#color').change(function() {
      var selectedColor = $(this).val();

      $.ajax({
        type: 'POST',
        url: '/actualizar',
        data: { color: selectedColor },
        success: function(response) {
          console.log(response);
          // Aquí puedes actualizar la tabla o realizar otras acciones después de recibir la respuesta del servidor
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
  });