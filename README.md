Codigo (Baseline) en Colab:

https://colab.research.google.com/drive/1dVgI0Hvgi7lrXXJihwwEO6VFhEb3xMfv?usp=sharing

(hay que subir el dataset y el codigo, pues aqui corre de mi Google Drive)

Entrenando con 50 epocas, early stop de 3, y todos parametros default.

1. XML-Roberta-base (modelo usado en Baseline)




2. 


-----------

Inspectionar (F12), Console:

function ConnectButton(){
    console.log("Conectado"); 
    document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect").click() 
}
setInterval(ConnectButton,60000);