import os
import shutil

main_path = r'C:\Users\DELL\PycharmProjects\Tesis\imagenes_2'

parcelas_id = [i.split('_')[1] for i in os.listdir(main_path) if i.endswith('.tif')]
# print(set(parcelas_id))

for i in parcelas_id:
    try:
        os.makedirs(f"{main_path}\Parcela_{i}")
    except OSError:
        os.rmdir(f"{main_path}\Parcela_{i}")
        os.makedirs(f"{main_path}\Parcela_{i}")

for root, dir_, file in os.walk(main_path):
    print(root)
    for j in file:
        parcela_id = f"{j.split('_')[0]}_{j.split('_')[1]}"
        for k in dir_:
            if parcela_id == k:
                # print(j, k)
                shutil.move(os.path.join(main_path, j), f"{main_path}\{k}\{j}")
