 How to install PhantomJS on Ubuntu

Version: `2.1.1`

Platform: `x86_64`

First, install or update to the latest system software.
```bash
sudo apt-get update
sudo apt-get install build-essential chrpath libssl-dev libxft-dev
```

Install these packages needed by PhantomJS to work correctly.
```bash
sudo apt-get install libfreetype6 libfreetype6-dev
sudo apt-get install libfontconfig1 libfontconfig1-dev
```

Get it from the [PhantomJS website](http://phantomjs.org/).
```bash
cd ~
export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"
wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2
sudo tar xvjf $PHANTOM_JS.tar.bz2
```

Once downloaded, move Phantomjs folder to `/usr/local/share/` and create symlinks:
```bash
sudo mv $PHANTOM_JS /usr/local/share
sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/share/phantomjs
sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin/phantomjs
sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/bin/phantomjs
```

Now, It should have PhantomJS properly on your system.
```bash
phantomjs --version
```

This is a modified version of [this script](https://gist.github.com/julionc/7476620)
