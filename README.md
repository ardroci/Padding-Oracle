# Padding-Oracle

Nos protocolos de rede é geralmente uma boa prática enviar uma mensagem de erro significativa aos clientes. Contudo em criptografia não é esse o caso, o conhecimento de que um determinado criptograma produz ou não um texto limpo com preenchimento válido contém informação suficiente para que o atacante consiga quebrar o esquema de cifra.

Com base nesta premissa, este projeto consistiu na decifra de um criptograma sem conhecimento da chave cifra utilizada. Para cumprir esse objetivo é enviado um conjunto de criptogramas a um oráculo que informa sobre o estado de validade do preenchimento após a decifra.


Criptograma
070707000304070777627d63716f737300120601080a18077d7f7c6969736d751e181a49011e18011a73722a606a7103

Texto Limpo
thecryptohobyistmayhaveread historical
