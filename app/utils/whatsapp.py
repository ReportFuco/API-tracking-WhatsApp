from io import BytesIO
from typing import Literal
import base64
import httpx


class BotWhatsApp:
    """
    Esta clase te ayuda a utilizar Evolution api a través de Python de manera sencilla, 
    permitiendo enviar mensajes y fotos.
    si no tienes creada una instancia de Evolution API, debes dirigirte al siguiente aca: 
    
    [Docummentación de Evolution API](https://doc.evolution-api.com/v1/en/get-started/introduction)
    """

    def __init__(
            self,
            url:str,
            instance:str,
            api_key:str
        ):
        
        self.url = url
        self.instance = instance
        self.api_key = api_key

    @property        
    def _headers(self):
        return {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }

    def enviar_mensaje(
            self, 
            numero:str, 
            mensaje:str,
            delay:int | None = None
        )->dict[Literal["info", "error", "status"], str]:
        """
        Envía un mensaje de texto a un número específico usando Evolution API.

        Args:
            numero (int): Número de teléfono en formato internacional (ej: 569...).
            mensaje (str): Texto que deseas enviar.

        Returns:
            None
        """
        

        try:
            if not delay:

                res = httpx.post(
                        f"{self.url}/message/sendText/{self.instance}",
                        headers=self._headers,
                        json={
                            "number": numero,
                            "text": mensaje,
                        }
                    )
            else:
                    res = httpx.post(
                    f"{self.url}/message/sendText/{self.instance}",
                    headers=self._headers,
                    json={
                        "number": numero,
                        "text": mensaje,
                        "delay":delay,
                    }
                )
            
            if res.status_code == 201:
                return {"status": "respuesta enviada"}
            else:
                return {
                    "status": f"El mensaje no fue enviado {res.status_code}",
                    "error": f"{res.text}"
                }
            
        except httpx.HTTPError as e:
            return {
                "error": f"error al enviar la informacion: {e}"
            }

    def enviar_mensaje_con_boton(
            self,
            numero:str,
            titulo:str,
            descripcion:str,
            footer:str,
            botones:list[str],
        )->dict[Literal["status", "error", "info"], str]:
        """
        Envía un mensaje de texto con botones personalizables a un número específico usando Evolution API.
        >>> Nota: Debes tener WhatsApp Bussines para poder enviar este mensaje.

        Args:
            numero (int): Número de teléfono en formato internacional (ej: 569...).
            titulo (str): Título del mensaje que quieres enviar.
            descripcion (str): cuerpo del mensaje que quieres enviar.
            footer (str): es el pie del mensaje que quieres enviar.
            botones (list): es una lista con los botones a utilizar dentro del mensaje.

        Returns:
            None
        """

        try:
            res = httpx.post(
                    f"{self.url}/message/sendButtons/{self.instance}",
                    headers=self._headers,
                    json={
                        "number": numero,
                        "title": titulo,
                        "description": descripcion,
                        "footer": footer,
                        "buttons": botones
                    }
                )
            
            if res.status_code == 201:
                return {"info": f"mensaje enviado: {res.status_code}"}
            
            else:
                return {
                    "status": f"El mensaje no fue enviado {res.status_code}",
                    "error": f"{res.text}"
                }
            
        except httpx.HTTPError as e:
            return {
                "error": f"error al enviar la informacion: {e}"
            } 

    def enviar_sticker(
            self,
            numero:int,
            sticker:str,
            delay:int | None = None
    
    )->dict[Literal["info", "error", "status"], str]:
        """
        Envía una sticker a un número específico usando Evolution API.

        Args:
            numero (int): Número de teléfono en formato internacional (ej: 569...).
            sticker (str): archivo en base64
            

        Returns:
            bool: True si se envió correctamente, False en caso de error.
        """
        try:
            if not delay:

                res = httpx.post(
                    f"{self.url}/message/sendSticker/{self.instance}",
                    headers=self._headers,
                    json={
                        "number": numero,
                        "sticker": sticker,
                        "delay": delay
                    }
                )
            
            else:

                res = httpx.post(
                    f"{self.url}/message/sendSticker/{self.instance}",
                    headers=self._headers,
                    json={
                        "number": numero,
                        "sticker": sticker,
                    }
                )
            
            if res.status_code == 201:
                return {"info": f"Sticker enviado: {res.status_code}"}
            
            else:
                return {
                    "status": f"El sticker no fue enviado {res.status_code}",
                    "error": f"{res.text}"
                }
            
        except httpx.HTTPError as e:
            return {
                "error": f"error al enviar la informacion: {e}"
            } 
        

    def enviar_mensaje_foto(
            self,
            numero:str,
            mensaje: str,
            path_foto:str | None = None,
            buffer:BytesIO | None = None,
            delay:int | None = None
        )->dict[Literal["info", "status", "error"], str]:
        """
        Envía una foto a un número específico usando Evolution API.

        Args:
            numero (int): Número de teléfono en formato internacional (ej: 569...).
            mensaje (str): Texto que deseas enviar.
            path_foto (str): Path del directorio de la foto que quieres enviar.
            buffer (BytesIO): Buffer de la foto que quieres enviar en el caso de que solo trabajes con memoria.

        Returns:
            bool: True si se envió correctamente, False en caso de error.
        """
        img:str = ""

        if path_foto and buffer:
            raise ValueError("Solo puedes proporcionar 'path_foto' o 'buffer', no ambos.")
    
        if not path_foto and not buffer:
            raise ValueError("Debes proporcionar al menos 'path_foto' o 'buffer'.")

        if buffer:

            buffer.seek(0)
            img = base64.b64encode(buffer.read()).decode("utf-8")   
            
        elif path_foto:
            
            with open(path_foto, "rb") as file:
                img = (base64.b64encode(file.read())
                    .decode("utf-8")
                )

        try:
            if not delay:
                res = httpx.post(
                    f"{self.url}/message/sendMedia/{self.instance}",
                    headers=self._headers,
                    json={
                        "media": img,
                        "caption": mensaje,
                        "mediatype": "image",
                        "number": numero,
                        "mimetype": "image/jpeg",
                        "delay": delay
                    },
                )
            else:
                res = httpx.post(
                    f"{self.url}/message/sendMedia/{self.instance}",
                    headers=self._headers,
                    json={
                        "media": img,
                        "caption": mensaje,
                        "mediatype": "image",
                        "number": numero,
                        "mimetype": "image/jpeg",
                    },
                )
            if res.status_code == 201:
                return {"info": f"Imangen enviado: {res.status_code}."}
            
            else:
                return {
                    "status": f"La imagen no fue enviada {res.status_code}.",
                    "error": f"{res.text}"
                }
            
        except httpx.HTTPError as e:
            return {
                "error": f"error al enviar la informacion: {e}"
            }