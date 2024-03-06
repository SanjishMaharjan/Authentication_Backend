import cloudinary
import cloudinary.uploader


cloudinary.config(
    cloud_name="dmvaqli9o",
    api_key="738932784514239",
    api_secret="b0WziKMdJCTfgBqayQPIqdT_8tM",
)


async def upload_file(file_path):
    result = cloudinary.uploader.upload(
        file_path, transformation=[{"width": 150, "height": 150, "crop": "thumb"}]
    )

    return result
    # return cloudinary.uploader.upload(file_path)
