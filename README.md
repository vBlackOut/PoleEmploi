# PoleEmploi
Robots PoleEmploi Selenium Python  

![alt text](http://alloemploi.fr/img/logo-pole-emploi.png)  

## video 
[![Watch the video](http://img.youtube.com/vi/KfOyb2EXQnY/0.jpg)](https://youtu.be/KfOyb2EXQnY)  
[![Watch the video](http://img.youtube.com/vi/uXtCLqZzZvU/0.jpg)](https://youtu.be/uXtCLqZzZvU)


## Functionnality
```
- auto login
- actualisation account
- get cv information
- search post recrute
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
# Firefox > 49.0
```

## For run
```
# edit config_bot.py
python3 main.py -p your_profile check

# check information cv number visitors/proposale appointment 
python3 main.py -p your_profile cv
```

## for fedora use selinux [sudo requirement]
```
sudo python3 main.py -p your_profile [check|cv]
```


