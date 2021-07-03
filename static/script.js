
function validarDados(){
    const input = document.getElementsByTagName("input");
    for (const campo of input){
        
        if (campo.value == ""){
            // const erro = document.getElementById("erro_create");
            // erro.classList.remove("erro_create");
            alert('Preencha todos os campos');
            return 
        }
    }
}

const enviarDados = document.getElementById("enviar_dados");
enviarDados.addEventListener("click", validarDados);

