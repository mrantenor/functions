from astroquery.vizier import Vizier
import pandas as pd
import numpy as np

def hipparcos(columns=['HIP','B-V','Vmag','Plx','e_Plx','RAhms','DEdms'],):
    """
    CATÁLOGO: 'I/239/hip_main'

    COLUMNS: ['HIP','B-V','Vmag','Plx','e_Plx','RAhms','DEdms']
    """    
    dt = pd.DataFrame(Vizier(columns=columns,row_limit = -1).get_catalogs('I/239/hip_main')[0].to_pandas())
    dt = dt.replace([0,[np.inf],[-np.inf],r'^\s*$'], np.nan, regex=True) #substitui vazios por nan
    dt = dt.dropna() #Limpa os nan

    dt['Mv'] = dt['Vmag'] + 5 * np.log10(dt['Plx']/100.) #magnitude para filtro V
    dt['L'] =  10**((4.83 - dt['Mv'])*0.4) #Luminosidade
    dt['Teff'] = 4600*((1/((0.92*dt['B-V'])+1.7))+(1/((0.92*dt['B-V'])+0.62))) #Temperatura Effetiva

    dt = dt.replace([0,[np.inf],[-np.inf],r'^\s*$'], np.nan, regex=True) #substitui vazios por nan
    dt = dt.dropna() #Limpa os nan
    return dt
    
def err_plx(dados,erro):
    dados['erro'] = dados['e_Plx']/dados['Plx']
    mask = dados['erro'] <= erro
    return dados[mask]