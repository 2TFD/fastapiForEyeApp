from gradio_client import Client, handle_file
async def modelGeneration(photo, token):
    client = Client("tencent/Hunyuan3D-2", hf_token=token)
    result = client.predict(
    caption="Пример описания",  # Текстовое описание (опционально)
    image=handle_file(photo),  # Путь к изображению
    steps=50,  # Количество шагов генерации
    guidance_scale=5.5,  # Масштаб направляющего сигнала
    seed=1234,  # Зерно для воспроизводимости
    octree_resolution="256",  # Разрешение октодерева
    check_box_rembg=True,  # Удаление фона
    api_name="/shape_generation"
    )
    return result[0]['value']

async def imageGeneration(promt, token):
    client = Client("stabilityai/stable-diffusion", hf_token=token)
    result = client.predict(
	prompt=promt,
	negative="null",
	api_name="/infer"
    )
    print(result[0]['image']),
    print(result[1]['image']),
    print(result[2]['image']),
    print(result[3]['image']),
    return result
    



async def chatGeneration(promt, token):
    client = Client("tencent/Hunyuan-T1", hf_token=token)
    result = client.predict(
	message=promt,
	api_name="/chat"
    )
    return result


async def musicGeneration(promt, token, style):
    client = Client("Adiwanwade/AI_Music_Generator", hf_token=token)
    result = client.predict(
	prompt=promt,
	style=style,
	duration=10,
	temperature=0.8,
	api_name="/predict"
    )
    return result