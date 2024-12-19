import yaml
from calc import mahjong_calc

def loadyaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    path = 'config.yaml'
    gameinfo = loadyaml(path)
    mahjong_calc(gameinfo)
    

if __name__ == '__main__':
    main()