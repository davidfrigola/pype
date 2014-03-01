# Installation shell script

# Install redis server
aptitude -y install redis-server redis-cli

# Configure redis
# Copy conf file with 0.0.0.0 for allowed IP
cp /vagrant/shared/redis.conf /etc/redis/
