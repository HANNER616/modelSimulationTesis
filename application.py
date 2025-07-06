# main.py

from fastapi import FastAPI, WebSocket
import uvicorn
import random
from datetime import datetime, timedelta



app = FastAPI()




@app.websocket("/video-stream")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    frame_count = 0


    try:
        while True:
            # Espera texto (el cliente envía JSON con { image: "<base64>" })
            msg = await websocket.receive_text()
            frame_count += 1
            confident_value = random.uniform(0.6, 0.8)

            if frame_count >= 25:
                frame_count = 0
                # Aquí podrías generar alertas de prueba
                alerts = [
                    {
                        "type": "motion",
                        "timestamp": (datetime.utcnow() - timedelta(hours=5)).isoformat() + "Z",
                        "description": "Movimiento sospechoso detectado en la cámara",
                        "confidence": confident_value,
                        "frame" : msg
                    }
                ]
                await websocket.send_json({ "alerts": alerts })

    except Exception:
        # Si se cierra la conexión o hay error, simplemente salimos
        await websocket.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("application:app", host="0.0.0.0", port=8080)
