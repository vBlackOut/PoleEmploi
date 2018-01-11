# PoleEmploi
Robots PoleEmploi Selenium Python  

![alt text](http://alloemploi.fr/img/logo-pole-emploi.png)  

## video 
[![Watch the video](http://img.youtube.com/vi/KfOyb2EXQnY/0.jpg)](https://youtu.be/KfOyb2EXQnY)


## Functionnality
```
- auto login
- actualisation account
- get cv information
```

## Testing environnement
```
- the script as tested for linux ( fedora 25 64bits)
```


## Requirement
```
# Python 3.x
# selenium ( sudo python3 -m pip install selenium )
# Pillow   ( sudo python3 -m pip install Pillow )
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

## for fedora 27-beta use sudo
```
sudo python3 main.py -p your_profile [check|cv]
```


