// obtenerDataType.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que se encarga de enviar el dataType al backend para obtener los datos correspondientes. 
    Se encarga de manejar las llamadas a la API y enviar los datos al servidor.
    Dependinedo del dataType se obtendrán los datos correspondientes.
        
*/ 


document.addEventListener("DOMContentLoaded", function(){
    const modalButtons = document.querySelectorAll(".modal-trigger");

    modalButtons.forEach(button =>{
        button.addEventListener("click", function(){
            const dataType = this.getAttribute("data-type")
            sendDataServer(dataType);
        })
    })

    function sendDataServer(dataType){
        const endpointURL =`/report/`

        fetch(endpointURL,{
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            //Json de lo que se manda al backend
            body: JSON.stringify({data_type: dataType})
        })
        .then(response => response.json())
        .catch((error)=>{
            console.error("Error:",error)
        })
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

})