//mostrarModals.js
let currentPage = 1; // Variable para almacenar la página actual
let allClientes = []; // Variable para almacenar todos los clientes
const modal = document.getElementById("genericModal");
const modalLabel = modal.querySelector(".modal-title");
const modalContent = modal.querySelector("#genericModalContent");
const modalFooter = modal.querySelector("#genericModalPagination");
const categoria_reporte = document
  .getElementById("categoria_reporte")
  .textContent.trim();
const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();

document.querySelectorAll(".modal-trigger").forEach(function (button) {
  button.addEventListener("click", function (e) {
    e.preventDefault();
    const dataType = this.getAttribute("data-type");
    currentPage = 1; // Resetear la página actual
    loadModalContent(dataType, currentPage, categoria_reporte, tipo_reporte);
  });
});

function loadModalContent(
  dataType,
  pageNumber,
  categoria_reporte,
  tipo_reporte
) {
  const csrftoken = getCookie("csrftoken");
  const reportUrl = `/report/?categoria_reporte=${encodeURIComponent(
    categoria_reporte
  )}&tipo_reporte=${encodeURIComponent(
    tipo_reporte
  )}&data_type=${encodeURIComponent(dataType)}&page=${pageNumber}`;

  fetch(reportUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      data: dataType,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.Clientes) {
        allClientes = result.Buscador;
        console.log("allClientes:", allClientes);
        modalContent.innerHTML = renderClientes(result.Clientes);
        modalFooter.innerHTML = renderPagination(
          result.Pagination,
          pageNumber,
          dataType
        );
        $("#genericModal").modal("show");
      } else {
        modalContent.innerHTML = "<p>No hay datos disponibles.</p>";
      }
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
      modalContent.innerHTML = "<p>Error al cargar el contenido.</p>";
    });
}

function buscador(dataType) {
  let input = document.getElementById("inputBusqueda");
  let filter = input.value.toUpperCase();

  // Si el campo de búsqueda está vacío, volver a cargar la página inicial
  if (filter === "") {
    loadModalContent(dataType, 1, categoria_reporte, tipo_reporte);
    return;
  }

  let filterClientes = allClientes.filter(
    (cliente) =>
      cliente.clave_cliente.toUpperCase().includes(filter) ||
      cliente.nombre_cliente.toUpperCase().includes(filter)
  );

  let ul = document.querySelector(".list-group");
  ul.innerHTML = "";

  if (filterClientes.length > 0) {
    filterClientes.forEach((cliente) => {
      let li = document.createElement("li");
      li.className = "list-group-item";
      li.textContent = `${cliente.clave_cliente} - ${cliente.nombre_cliente}`;
      ul.appendChild(li);
    });
  } else {
    ul.innerHTML = "<li class='list-group-item'>No se encontraron resultados.</li>";
  }
}

function renderClientes(clientes, dataType) {
  let html = "";

  html += `
        <div class="search-container d-flex">
            <svg style="margin-top: auto; margin-bottom: auto; padding-right:5px;" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.3-4.3"/>
            </svg>
            <input style="margin-top: auto; margin-bottom: auto" class="rounded search-input" type="text" id="inputBusqueda" onkeyup="buscador('${dataType}')" placeholder="Buscar clientes...">
        </div>
    `;

  html += '<ul class="list-group mt-3">';
  clientes.forEach((cliente) => {
    html += `<li class="list-group-item">${cliente.clave_cliente} - ${cliente.nombre_cliente}</li>`;
  });
  html += "</ul>";

  return html;
}

function renderPagination(paginationData, currentPage, dataType) {
  let html = '<nav aria-label="Page navigation">';

  html += '<ul class="pagination justify-content-center">';

  html += '<li class="page-item">';

  if (paginationData && paginationData.has_previous) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', 1, '${categoria_reporte}', '${tipo_reporte}')" aria-label="First"><span aria-hidden="true">&laquo;</span></a>`;
  } else {
    html +=
      '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&laquo;</span></span>';
  }

  html += "</li>";

  html += '<li class="page-item">';

  if (paginationData && paginationData.has_previous) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', ${paginationData.previous_page_number}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Previous"><span aria-hidden="true">&lt;</span></a>`;
  } else {
    html +=
      '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&lt;</span></span>';
  }

  html += "</li>";

  html += '<li class="page-item disabled">';
  html += `<span class="page-link">Page ${currentPage} of ${paginationData.num_pages}</span>`;
  html += "</li>";

  html += '<li class="page-item">';
  if (paginationData && paginationData.has_next) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', ${paginationData.next_page_number}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Next"><span aria-hidden="true">&gt;</span></a>`;
  } else {
    html +=
      '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&gt;</span></span>';
  }
  html += "</li>";

  html += '<li class="page-item">';
  if (paginationData && paginationData.has_next) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', ${paginationData.num_pages}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Last"><span aria-hidden="true">&raquo;</span></a>`;
  } else {
    html +=
      '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&raquo;</span></span>';
  }
  html += "</li>";

  html += "</ul>";
  html += "</nav>";

  return html;
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
