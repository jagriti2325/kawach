import torch
pth='models/tb_model.pth'
loaded=torch.load(pth,map_location='cpu')
print(type(loaded))
if isinstance(loaded, dict):
    print('keys', list(loaded.keys())[:10])
    d = loaded.get('state_dict', loaded.get('model', loaded))
else:
    d = loaded
print('num keys', len(d))
for key in list(d.keys())[:25]:
    print(key)
