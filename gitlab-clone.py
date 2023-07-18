import os
import gitlab
import subprocess

gl = gitlab.Gitlab(private_token='PERSONAL-ACCESS-TOKEN-HERE')

ssh_urls = []
parents = []
groups = gl.groups.list()

# itera em todos os grupos e cria uma lista com todos os projetos
for group in groups:
  projects = group.projects.list()
  for p in projects:
    # cria uma lista com todos os links ssh para clonar projeto
    ssh_urls.append(p.ssh_url_to_repo)
    # cria uma lista com todos os parent paths de cada repo
    parents.append(p.namespace['full_path'])

# cria dicionario relacionando as duas listas
urls_caminhos = dict(zip(ssh_urls, parents))

# inserir caminhos na variavel caminho_default, caminho onde repos devem ser adicionados
caminho_default = 'DEFAULT_BEGINNING_PATH'

# cria diretorios e clona os repos dentro deles
for url, caminho in urls_caminhos.items():
  os.chdir(caminho_default)

  # INSERIR AQUI CAMINHO DO GRUPO OU SUBGRUPO A SER CLONADO - path deve começar da raiz dos grupos
  if caminho.startswith('GROUP_PATH_TO_CLONE_FROM'):
    # cria diretorio com caminho novo, caso nao exista
    try:
      os.makedirs(caminho)
    except:
      print("Caminho já existe, mudando de diretório...")
    
    # muda para diretorio e clona repo
    os.chdir(caminho)
    return_code = subprocess.call(['git', 'clone', url])
    if return_code == 0:
      print("Repositório clonado com sucesso.")
    else:
      print("Command failed with return code", return_code)