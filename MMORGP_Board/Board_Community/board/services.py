def get_path_upload_image(instance, file):
    date = instance.datetime_in.strftime('%d_%m_%Y %H_%M')
    return f'photo/post/{date}/{file}'


def get_path_upload_video(instance, file):
    date = instance.datetime_in.strftime('%d_%m_%Y %H_%M')
    return f'video/post/{date}/{file}'
