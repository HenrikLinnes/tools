# d = {"asset_name": ["a","b", "c"],
#       "icon_path": ["test/a", "test/b", "test/c"],
#       "cpio_path": ["a.cpio", "b.cpio", "c.cpio"]}

asset_name = ["test1", "test2", "test3", "test4"]
icon_path = ["1.jpg", "2.jpg", "3.jpg", "4.jpg"]
cpio_path = ["1.cpio", "2.cpio", "3.cpio", "4.cpio"]

d= {}
for idx in range (len(asset_name)):
    # d = {idx+1: {"asset_name": asset_name[idx], "icon_path": icon_path[idx], "cpio_path": cpio_path[idx]}}
    d[asset_name[idx]] = {}
    d[asset_name[idx]]["asset_name"] = asset_name[idx]
    d[asset_name[idx]]["icon_path"] = icon_path[idx]
    d[asset_name[idx]]["cpio_path"] = cpio_path[idx]

print(d)

# for idx, key in enumerate(d.keys()):
#     print(d["asset_name"][idx], d["icon_path"][idx], d["cpio_path"][idx] )





# path = r"T:/assetLibrary/houdini_assets/NodeSnippet/Test/Test.jpg"

# import requests
# from fancy_tools.utils import requests_file

# s = requests.Session()
# s.mount('file://', requests_file.FileAdapter())

# resp = s.get('file:///T:/assetLibrary/houdini_assets/NodeSnippet/Test')

# print(resp)