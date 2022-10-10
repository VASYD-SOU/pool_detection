import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from pyproj import Transformer

# See other answer about the always_xy=True parameter
TRAN_3008_TO_4326 = Transformer.from_crs("EPSG:3008", "EPSG:4326")

def mytransform(lat, lon):
  return TRAN_3008_TO_4326.transform(lat, lon)

box_df = pd.read_csv(r'P:\Workspace\pool_detection\pool_boxes_075.csv')
box_df['wld_path'] = box_df['path'].str.replace('jpg', 'wld')

adress_df = pd.read_csv(r'P:\Workspace\pool_detection\Adresser_Malmö.csv', sep=';', encoding='latin', dtype=str)
adress_df = adress_df[['Beladress', 'Xkoord', 'Ykoord']]
adress_df['Xkoord'] = pd.to_numeric(adress_df['Xkoord'].astype(str).str.replace(',', '.'))
adress_df['Ykoord'] = pd.to_numeric(adress_df['Ykoord'].astype(str).str.replace(',', '.'))
adress_list = adress_df['Beladress'].tolist()

adress_coords = []
for k in range(len(adress_df)):
    adress_coords.append([adress_df['Xkoord'][k], adress_df['Ykoord'][k]])

adress_coords = np.array(adress_coords)

shortest_dist_list = [None]*len(adress_list)
for i in range(len(box_df)):
    box = [box_df['startX'][i], box_df['startY'][i], box_df['endX'][i], box_df['endY'][i]]
    x_pixel = (box_df['startX'][i] + box_df['endX'][i])/2
    y_pixel = (box_df['startY'][i] + box_df['endY'][i])/2

    path = box_df['path'][i]
    wld_path = box_df['wld_path'][i]

    with open(wld_path) as WorldFile:
        a = float(WorldFile.readline())
        d = float(WorldFile.readline())
        b = float(WorldFile.readline())
        e = float(WorldFile.readline())
        c = float(WorldFile.readline())
        f = float(WorldFile.readline())

    y_coord = a*x_pixel + b*y_pixel + c
    x_coord = d*x_pixel + e*y_pixel + f

    pool_coords = np.array([[x_coord, y_coord]])
    dist_list = cdist(pool_coords, adress_coords)
    shortest_dist = np.min(dist_list)
    dist_index = np.where(dist_list==shortest_dist)[1][0]
    shortest_dist_list[dist_index] = shortest_dist

pool_df = pd.DataFrame(list(zip(adress_list, shortest_dist_list)), columns =['adress', 'distance'])
pool_df.dropna(inplace=True)
pool_df = pool_df.loc[pool_df['distance'] <= 30]

adress_df.rename(columns = {'Beladress' : 'adress'}, inplace=True)
pool_df = pd.merge(pool_df, adress_df, on='adress', how='left')

pool_df['adress'] = pool_df['adress'].str.rstrip()
pool_df['adress'] = pool_df['adress'].str.lstrip()
pool_df.drop(columns=['distance'], inplace=True)


fastighetstyp_df = pd.read_csv(r'P:\Workspace\pool_detection\EDP_alla.csv')
fastighetstyp_df = fastighetstyp_df.loc[fastighetstyp_df['Faktgrupp'] == 'MALMÖ']
fastighetstyp_df = fastighetstyp_df[['Anladress', 'Anlkat']]
fastighetstyp_df.rename(columns={'Anladress':'adress', 'Anlkat':'Fastighetstyp'}, inplace=True)
fastighetstyp_df['adress'] = fastighetstyp_df['adress'].str.upper()
fastighetstyp_df['adress'] = fastighetstyp_df['adress'].str.rstrip()
fastighetstyp_df['adress'] = fastighetstyp_df['adress'].str.lstrip()

pool_df = pd.merge(pool_df, fastighetstyp_df, on='adress', how='left')
pool_df = pool_df.loc[pool_df['Fastighetstyp'] == 'VILLA']
pool_df.drop_duplicates(inplace=True)

x_list = pool_df['Xkoord'].to_list()
y_list = pool_df['Ykoord'].to_list()

x_coord_4326 = []
y_coord_4326 = []
for i in range(len(x_list)):
    coords_4326 = mytransform(x_list[i], y_list[i])
    x_coord_4326.append(coords_4326[0])
    y_coord_4326.append(coords_4326[1])

pool_df['Xkoord'] = x_coord_4326
pool_df['Ykoord'] = y_coord_4326

pool_df.drop(columns=['Fastighetstyp'], inplace=True)

pool_df.to_csv(r'P:\Workspace\pool_detection\adresser_med_pool_malmö_075.csv', encoding='latin', index=False)