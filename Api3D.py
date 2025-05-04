async def generate3d(photo, token):
    from gradio_client import Client, handle_file
    
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
    # print(result[0]['value'])
    return result[0]['value']

