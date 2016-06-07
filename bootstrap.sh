apt-get update
apt-get install -y python-setuptools
easy_install pip
pip install virtualenv virtualenvwrapper

su vagrant <<'EOF'
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
export PIP_VIRTUALENV_BASE=$WORKON_HOME

echo "export WORKON_HOME=$HOME/.virtualenvs" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
echo "export PIP_VIRTUALENV_BASE=$WORKON_HOME" >> /home/vagrant/.bashrc

mkvirtualenv get-leads
workon get-leads

cd /vagrant/
pip install -r requirements.txt
EOF
