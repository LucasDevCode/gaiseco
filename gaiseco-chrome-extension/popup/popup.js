console.log("DEBUG FROM popup");

const server_address = 'http://127.0.0.1:5000/'

// Verificando conexão.
fetch(server_address + 'ping')
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then((data) => {
    if (data == 'pong') {
        document.getElementById('text-status').innerText = "Conectado";
    } else {
        document.getElementById('text-status').innerText = "Não Conectado";    
    }
  })
  .catch((error) => {
    document.getElementById('text-status').innerText = "Não Conectado";
    console.error("Error:", error);
  });







// const response = await fetch(server_address + 'ping');

// const p_tag = document.getElementById('text-status');

// if (response.ok == true) {
//     const json = await response.json();
    
//     if (json == 'pong') {
//         p_tag.innerText = "Conectado";
//     } else {
//         p_tag.innerText = "Não Conectado";
//         tag.classList.add('inactive');
        
//         console.log('error')    
//     }

// } else {
//     p_tag.innerText = "Não Conectado";
//     console.log('error');
// }