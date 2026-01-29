import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset(dataset_id, target_path):
    api = KaggleApi()
    api.authenticate()
    
    # Garante que a pasta existe
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # O método 'dataset_download_files' com unzip=True 
    # geralmente sobrescreve arquivos existentes com o mesmo nome.
    print(f"Baixando {dataset_id} em {target_path}...")
    api.dataset_download_files(dataset_id, path=target_path, unzip=True)
    print("Download e extração concluídos!")
def main():
    download_dataset('teocalvo/teomewhy-loyalty-system', 'loyalty_system/' )
    download_dataset('teocalvo/teomewhy-education-platform', 'education_platform/' )
# Uso:
if __name__ == "__main__":
    main()