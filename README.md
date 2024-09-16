# llm-parser
A simple LLM parser to handle potential errors when responses don't match the expected format.

# LlmParser

La clase LlmParser posee un constructor "format" con la idea de que en el futuro se puedan implementar otros formatos. Por ahora solo utiliza un formateador de Json.

Para parsear la respuesta del llm simplemente usa el metodo .parse() o .parse_with_keys()

El formato de retorno es:
```JSON
{
    'json': <El json real que se espera>,
    'state': <un string con un código que indica potenciales errores>
}
```

Para obtener el json simplemente accede a él:
```python
llm_answer = "<la respuesta del llm>"
parser = LlmParser()

expected_json = parser.parse(llm_answer)['json']
```

De igual manera se puede acceder al 'state' del parseo. Los posibles mensajes obtenidos son:
- VALID: Indica que solo se recibio un json. En este caso se podría haber utilizado la respuesta del llm directamente con json.loads y hubiese funcionado sin errores.
- ERROR_EXTRA_TEXT: En este caso había un json valido dentro del string devuelto, pero había texto extra. El texto se extrajo y se devolvió el resto del json.
- ERROR_INVALID_JSON: En este caso no hubo forma de reconstruir el json esperado. Por tanto se devuelve vacio {}.
- MISSING_KEYS: Solo si se usa con parse_with_keys indica si al json obtenido le falta alguna de las keys dadas.