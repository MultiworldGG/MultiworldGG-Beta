from kivy.core.image import ImageData, ImageLoader, ImageLoaderBase
import typing
import io

class ImageLoaderPkgutil(ImageLoaderBase):
    def load(self, filename: str) -> list[ImageData]:
        import re

        filename = filename[7:]
        print(filename)
        parentPath, childPath = filename.split("zip/", 1)
        childPath = re.sub(r"^\/*", "", childPath)
        import zipfile
        with zipfile.ZipFile(parentPath+"zip") as parentSource:
            with parentSource.open(childPath) as childSource:
                return self._bytes_to_data(childSource.read())

    @staticmethod
    def _bytes_to_data(data: typing.Union[bytes, bytearray]) -> typing.List[ImageData]:
        loader = next(loader for loader in ImageLoader.loaders if loader.can_load_memory())
        return loader.load(loader, io.BytesIO(data))      


# grab the default loader method so we can override it but use it as a fallback
_original_image_loader_load = ImageLoader.load

def load_override(self, filename: str, default_load=_original_image_loader_load, **kwargs):
    if filename.startswith("ap:zip:"):
        return ImageLoaderPkgutil.load(self, filename)
    else:
        return default_load(self, filename, **kwargs)

ImageLoader.load = load_override