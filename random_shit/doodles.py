d = {"asset_name": ["a","b", "c"],
      "icon_path": ["test/a", "test/b", "test/c"],
      "cpio_path": ["a.cpio", "b.cpio", "c.cpio"]}

for idx, key in enumerate(d.keys()):
    print(d["asset_name"][idx], d["icon_path"][idx], d["cpio_path"][idx] )





# path = r"T:/assetLibrary/houdini_assets/NodeSnippet/Test/Test.jpg"

# import requests
# from fancy_tools.utils import requests_file

# s = requests.Session()
# s.mount('file://', requests_file.FileAdapter())

# resp = s.get('file:///T:/assetLibrary/houdini_assets/NodeSnippet/Test')

# print(resp)