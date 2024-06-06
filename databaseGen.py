import json

def text_to_json(text):
    entries = []
    blocks = text.strip().split("\n\n")  # Separar bloques de preguntas y respuestas
    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 2:
            question = lines[0].replace("Pregunta:", "").strip()
            answer = "\n".join(lines[1:]).replace("Respuesta:", "").strip()
            entries.append({"from": "human", "value": question})
            entries.append({"from": "gpt", "value": answer})
    return json.dumps(entries, ensure_ascii=False, indent=2)

# Ejemplo de uso:
texto = """
Pregunta: ¿Qué constituye un Cuerpo Universitario según el documento?
Respuesta: Los titulares de ciudadanía de una misma categoría constituyen un Cuerpo Universitario y no se puede pertenecer simultáneamente a más de uno de ellos​​.

Pregunta: ¿Quién dictará la reglamentación sobre los derechos y obligaciones de la Ciudadanía Universitaria?
Respuesta: El Consejo Superior será el encargado de dictar la reglamentación sobre los derechos y obligaciones de la Ciudadanía Universitaria​​.

Pregunta: ¿Quién coordina la labor de los organismos que integran la Universidad?
Respuesta: El gobierno de la Universidad coordina la labor de los organismos que la integran​​.

Pregunta: ¿Cuáles son los órganos del gobierno universitario?
Respuesta: Los órganos del gobierno universitario son la Asamblea Universitaria, el Consejo Superior y el Rector​​.

Pregunta: ¿Qué es la Asamblea Universitaria?
Respuesta: La Asamblea Universitaria es el órgano superior de la Universidad, constituido por todos los miembros del Consejo Superior y los Consejos Directivos de las Facultades​​.

Pregunta: ¿Con qué frecuencia debe reunirse la Asamblea Universitaria?
Respuesta: La Asamblea Universitaria debe reunirse por lo menos una vez al año​​.

Pregunta: ¿Quién preside la Asamblea Universitaria?
Respuesta: El Rector o su reemplazante preside la Asamblea Universitaria​​.

Pregunta: ¿Qué sucede en caso de empate en las deliberaciones de la Asamblea Universitaria?
Respuesta: En caso de empate, el Presidente de la Asamblea Universitaria decide solo en caso de segundo empate​​.

Pregunta: ¿Cómo se realiza la convocatoria a la Asamblea Universitaria?
Respuesta: La convocatoria a la Asamblea Universitaria es realizada por el Rector o su reemplazante, previa decisión del Consejo Superior o a petición de un tercio de los miembros de aquella o de la mitad más uno de los Consejos Directivos​​.

Pregunta: ¿Cuál es el mínimo de anticipación para realizar la convocatoria a la Asamblea Universitaria?
Respuesta: La convocatoria debe hacerse con un mínimo de quince días de anticipación​​.

Pregunta: ¿Cuál es el quórum requerido para la Asamblea Especial según el Artículo 9 inciso c)?
Respuesta: El quórum requerido es de las tres cuartas partes de los integrantes del Cuerpo​​.

Pregunta: ¿Cuáles son las atribuciones de la Asamblea Universitaria?
Respuesta: Las atribuciones de la Asamblea Universitaria incluyen fijar la política universitaria, dictar o modificar el Estatuto, elegir Rector y Vicerrector, decidir sobre sus renuncias, y suspender o remover al Rector y Vicerrector por causas justificadas​​.

Pregunta: ¿Quiénes continuarán en sus cargos hasta la finalización de sus mandatos según el Artículo 303?
Respuesta: Los titulares de los órganos colegiados y unipersonales de gobierno de las instituciones universitarias nacionales, elegidos de acuerdo a los estatutos vigentes al momento de la sanción de la presente ley, continuarán en sus cargos hasta la finalización de sus respectivos mandatos​​.

Pregunta: ¿Qué deben hacer las autoridades universitarias dentro de los 180 días contados a partir de la fecha de publicación de los nuevos estatutos?
Respuesta: Las autoridades universitarias deben adecuar la integración de sus órganos colegiados de gobierno para que se respete la proporción establecida en el Artículo 53, inciso a)​​.

Pregunta: ¿Qué deben hacer las instituciones universitarias que ostenten el nombre de universidad y deban ser categorizadas como institutos universitarios?
Respuesta: Deben solicitar la nueva categorización en el plazo de un año contado a partir de la promulgación de la presente ley​​.

Pregunta: ¿Qué universidad conservará su denominación y categoría institucional actual según el Artículo 305?
Respuesta: La Universidad Tecnológica Nacional conservará su denominación y categoría institucional actual​​.

Pregunta: ¿Qué plazo tienen los centros de investigación e instituciones de formación profesional superior para adecuarse a la nueva legislación?
Respuesta: Tienen un plazo de dos años para adecuarse a la nueva legislación​​.

Pregunta: ¿Quién fiscalizará a los centros de investigación durante el periodo de adecuación a la nueva legislación?
Respuesta: El Ministerio de Cultura y Educación fiscalizará a los centros de investigación​​.

Pregunta: ¿Qué no podrá hacer el Poder Ejecutivo nacional hasta que se constituya el órgano de evaluación y acreditación?
Respuesta: No podrá implementar la organización de nuevas instituciones universitarias nacionales ni disponer la autorización provisoria o el reconocimiento definitivo de instituciones universitarias privadas​​.

Pregunta: ¿Qué artículo de la Ley de Ministerios fue sustituido por el Artículo 308?
Respuesta: El inciso 11) del Artículo 21 de la Ley de Ministerios fue sustituido​​.

Pregunta: ¿Qué prohíbe el Artículo 223 respecto a los estudios de grado en instituciones de gestión estatal?
Respuesta: Prohíbe establecer cualquier tipo de gravamen, tasa, impuesto, arancel o tarifa directos o indirectos sobre los estudios de grado​​.

Pregunta: ¿Qué tipo de acuerdos o convenios no pueden suscribir las instituciones de educación superior de gestión estatal?
Respuesta: No pueden suscribir acuerdos o convenios que impliquen ofertar educación como un servicio lucrativo o que alienten formas de mercantilización​​.

Pregunta: ¿Cuál es la finalidad de la educación superior según el Artículo 224?
Respuesta: La educación superior tiene la finalidad de proporcionar formación científica, profesional, humanística y técnica en el más alto nivel, contribuir a la preservación de la cultura nacional, promover el desarrollo del conocimiento y desarrollar actitudes y valores responsables, éticos y solidarios​​.

Pregunta: ¿Qué objetivos adicionales tiene la educación superior según el Artículo 225?
Respuesta: Entre los objetivos adicionales están formar científicos y profesionales comprometidos con la sociedad, preparar para la docencia en todos los niveles, promover la investigación y las creaciones artísticas, garantizar calidad y excelencia, y profundizar la democratización en la educación superior​​.

Pregunta: ¿Qué es la Comisión Nacional de Evaluación y Acreditación Universitaria?
Respuesta: Es un organismo descentralizado que funciona bajo la jurisdicción del Ministerio de Cultura y Educación y tiene funciones como coordinar la evaluación externa y acreditar carreras de grado y posgrado​​.

Pregunta: ¿Cuántos miembros integran la Comisión Nacional de Evaluación y Acreditación Universitaria y cómo son designados?
Respuesta: La comisión está integrada por doce miembros designados por el Poder Ejecutivo nacional a propuesta de varios organismos, y deben ser personalidades de reconocida jerarquía académica y científica​​.


"""

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

resultado_json = text_to_json(texto)
# Guardar el resultado en un archivo JSON
save_to_file(resultado_json, 'database.json')

print(resultado_json)
