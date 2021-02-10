def image_validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def zip_validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.zip']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def mp4_validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4','.ogg','.webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def ogg_validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.ogg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def webm_validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
