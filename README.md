Codigo (Baseline) en Colab:

https://colab.research.google.com/drive/1dVgI0Hvgi7lrXXJihwwEO6VFhEb3xMfv?usp=sharing

(hay que subir el dataset y el codigo, pues aqui corre de mi Google Drive)

Entrenando con 50 epocas, early stop de 3, y todos parametros default. Evaluated con dataset de dev.

1. XML-Roberta-base (modelo usado en Baseline)

Stopped at epoch 8

```
'ALLPRED': 1144.0,
 'ALLRECALLED': 976.0,
 'ALLTRUE': 1176.0,
 'F1@CORP': 0.8219178318977356,
 'F1@CW': 0.6432432532310486,
 'F1@GRP': 0.752293586730957,
 'F1@LOC': 0.8299817442893982,
 'F1@PER': 0.8721174001693726,
 'F1@PROD': 0.7361563444137573,
 'MD@F1': 0.8413792848587036,
 'MD@P': 0.8531468510627747,
 'MD@R': 0.8299319744110107,
 'P@CORP': 0.7947019934654236,
 'P@CW': 0.6685393452644348,
 'P@GRP': 0.7735849022865295,
 'P@LOC': 0.831501841545105,
 'P@PER': 0.904347836971283,
 'P@PROD': 0.7385621070861816,
 'R@CORP': 0.8510638475418091,
 'R@CW': 0.6197916865348816,
 'R@GRP': 0.7321428656578064,
 'R@LOC': 0.8284671306610107,
 'R@PER': 0.8421052694320679,
 'R@PROD': 0.7337662577629089,
 'loss': 5.141009330749512,
 'micro@F1': 0.7844827771186829,
 'micro@P': 0.7954545617103577,
 'micro@R': 0.773809552192688
 ```

1. BETO

Stopped at epoch 4

```
'ALLPRED': 1119.0,
 'ALLRECALLED': 964.0,
 'ALLTRUE': 1176.0,
 'F1@CORP': 0.8156028389930725,
 'F1@CW': 0.6166219711303711,
 'F1@GRP': 0.7371794581413269,
 'F1@LOC': 0.84112149477005,
 'F1@PER': 0.8888888955116272,
 'F1@PROD': 0.7197231650352478,
 'MD@F1': 0.8400871753692627,
 'MD@P': 0.8614834547042847,
 'MD@R': 0.819727897644043,
 'P@CORP': 0.8156028389930725,
 'P@CW': 0.6353591084480286,
 'P@GRP': 0.7986111044883728,
 'P@LOC': 0.8620689511299133,
 'P@PER': 0.8715953230857849,
 'P@PROD': 0.770370364189148,
 'R@CORP': 0.8156028389930725,
 'R@CW': 0.5989583134651184,
 'R@GRP': 0.6845238208770752,
 'R@LOC': 0.8211678862571716,
 'R@PER': 0.9068825840950012,
 'R@PROD': 0.6753246784210205,
 'loss': 4.607795238494873,
 'micro@F1': 0.7825707793235779,
 'micro@P': 0.8025022149085999,
 'micro@R': 0.7636054158210754,
```

1. BSC-TeMU/roberta-base-bne

```
Stopped at epoch 5

'ALLPRED': 1151.0,
 'ALLRECALLED': 919.0,
 'ALLTRUE': 1174.0,
 'F1@CORP': 0.753731369972229,
 'F1@CW': 0.6034482717514038,
 'F1@GRP': 0.7182662487030029,
 'F1@LOC': 0.7707979679107666,
 'F1@PER': 0.8370221257209778,
 'F1@PROD': 0.6000000238418579,
 'MD@F1': 0.7905376553535461,
 'MD@P': 0.798436164855957,
 'MD@R': 0.7827938795089722,
 'P@CORP': 0.7952755689620972,
 'P@CW': 0.6730769276618958,
 'P@GRP': 0.7483870983123779,
 'P@LOC': 0.7183544039726257,
 'P@PER': 0.8320000171661377,
 'P@PROD': 0.6122449040412903,
 'R@CORP': 0.716312050819397,
 'R@CW': 0.546875,
 'R@GRP': 0.6904761791229248,
 'R@LOC': 0.831501841545105,
 'R@PER': 0.8421052694320679,
 'R@PROD': 0.5882353186607361,
 'loss': 7.2361016273498535,
 'micro@F1': 0.7286021709442139,
 'micro@P': 0.7358818650245667,
 'micro@R': 0.7214650511741638
```

1. bert-base-multilingual-uncased

Stopped at epoch 7

```
'ALLPRED': 1194.0,
 'ALLRECALLED': 1017.0,
 'ALLTRUE': 1176.0,
 'F1@CORP': 0.800000011920929,
 'F1@CW': 0.7083333134651184,
 'F1@GRP': 0.7911392450332642,
 'F1@LOC': 0.8481675386428833,
 'F1@PER': 0.9036144614219666,
 'F1@PROD': 0.6990291476249695,
 'MD@F1': 0.8582278490066528,
 'MD@P': 0.8517587780952454,
 'MD@R': 0.8647959232330322,
 'P@CORP': 0.7785235047340393,
 'P@CW': 0.7083333134651184,
 'P@GRP': 0.8445945978164673,
 'P@LOC': 0.8127090334892273,
 'P@PER': 0.8964143395423889,
 'P@PROD': 0.6967741847038269,
 'R@CORP': 0.8226950168609619,
 'R@CW': 0.7083333134651184,
 'R@GRP': 0.7440476417541504,
 'R@LOC': 0.8868613243103027,
 'R@PER': 0.9109311699867249,
 'R@PROD': 0.701298713684082,
 'loss': 4.594475746154785,
 'micro@F1': 0.8042194247245789,
 'micro@P': 0.7981574535369873,
 'micro@R': 0.8103741407394409
```

-----------

Inspectionar (F12), Console:

```
function ConnectButton(){
    console.log("Conectado"); 
    document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect").click() 
}
setInterval(ConnectButton,60000);
```