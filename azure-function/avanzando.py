from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text import  TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError


def traducir_entrada(texto, key, endpoint,region,idiomadetectado):
    try:
            if not idiomadetectado=="en":
                credential = TranslatorCredential(key, region)
                text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

                source_language = idiomadetectado
                target_languages = ["en"]
                input_text_elements = [InputTextItem(text=texto)]
                response = text_translator.translate(content = input_text_elements, to = target_languages, from_parameter = source_language)

                translation = response[0] if response else None
                if translation:
                    for translated_text in translation.translations:
                        return {
                            #"prompt": translated_text.text
                            translated_text.text
                        }
    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

def main():
    # set `<your-key>`, `<your-endpoint>`, and  `<region>` variables with the values from the Azure portal

    key = "8Kv5ePPTjJCPyG1BCBOgXjhRr7jBYLy88MMpr4bWTdT6KWH8lPs8JQQJ99BCACYeBjFXJ3w3AAAbACOGAX5y"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    region = "eastus"


    idiomadetectado="es"
    texto=("Recuerda eliminar la clave de tu código cuando termines y nunca la publiques. "
           "Para la producción, utilice una forma segura de almacenar y acceder a sus credenciales, "
           "como Azure Key Vault. Para obtener más información, consulte Seguridad de los servicios de Azure AI.")

    texto_traducido=traducir_entrada(texto, key, endpoint, region, idiomadetectado)
    #print(f"Traduccion: {texto_traducido['prompt']}")
    print(f"Traduccion: {texto_traducido}")

if __name__ == "__main__":
    main()