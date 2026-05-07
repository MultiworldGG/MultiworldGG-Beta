# Why does this exist at all? It has a default zip loader if it's a zip file.



# from kivy.core.image import ImageLoaderBase, ImageLoader, ImageData

# class ImageLoaderTracker(ImageLoaderBase):

#     @staticmethod
#     def extensions():
#         return ('zip', )

#     def load(self, filename: str) -> list[ImageData]:
#         import re

#         filename = filename[7:]
#         print(filename)
#         parentPath, childPath = filename.split("zip/", 1)
#         childPath = re.sub(r"^\/*", "", childPath)
#         import zipfile
#         with zipfile.ZipFile(parentPath+"zip") as parentSource:
#             with parentSource.open(childPath) as childSource:
#                 return self._bytes_to_data(childSource.read())

# ImageLoader.register(ImageLoaderTracker)
