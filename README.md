# PoleEmploi
Robots PoleEmploi Selenium Python  

![alt text](http://alloemploi.fr/img/logo-pole-emploi.png)  

## video 
[<img src="http://img.youtube.com/vi/KfOyb2EXQnY/0.jpg" height="300" width="300">](https://www.youtube.com/watch?v=KfOyb2EXQnY&feature=youtu.be) [<img src="http://img.youtube.com/vi/uXtCLqZzZvU/0.jpg" height="300" width="300">](https://www.youtube.com/watch?v=uXtCLqZzZvU&feature=youtu.be)

## Images
![Image script](https://www.cuby-hebergs.com/dl/projet/polemplois.png)  

## Functionnality
```
- auto login
- actualisation account
- get cv information
- search post recrute
- send cv for offer jobs
```

## Testing environnement
```
- the script as tested for linux ( fedora 25/26/27 64bits)
```


## Requirement
```
# Python 3.x
# selenium ( sudo python3 -m pip install selenium )
# Pillow   ( sudo python3 -m pip install Pillow )
# BeautifullSoup ( sudo python3 -m pip install beautifullsoup )
# lxml ( sudo python3 -m pip install lxml ) 
# pyvirtualdisplay ( sudo python3 -m pip install pyvirtualdisplay ) 
# YAML (default package is installed but no install > sudo python3 -m pip install yaml) 
# Firefox > 49.0 
```

## For run
```
# edit config.yml
python3 main.py -p your_profile check

# check information cv number visitors/proposale appointment 
python3 main.py -p your_profile cv

# launch search job's
python3 main.py -p your_profile search
```

## for fedora use selinux [sudo requirement]
```
sudo python3 main.py -p your_profile [check|cv|search]
```


